from config import services,mode 
from time import sleep
from datetime import datetime, timedelta
from os import system,getuid
import logging

def init_check():
    if getuid() != 0:
        logging.error('need root permission! bye. 需要 root 权限！再见。')
        exit()
    if system('iptables -V') == 32512:
        logging.error('iptables not found. 没有找到 iptables 命令。')
        exit()

# https://stackoverflow.com/a/51928942
def flask_get_ip(request):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


def timeout_check(knocker):
    while True:
        sleep(1)
        for ip in knocker.copy():
            for service_name in knocker[ip].copy():
                expire_date = knocker[ip][service_name]['expire_date']
                if datetime.now() > expire_date:
                    iptables('del', ip, service_name)
                    knocker_edit('del', ip, service_name, knocker)


def knocker_edit(action, ip, service_name, knocker):
    logging.info(
        f'knocker_edit: action:{action}, ip:{ip}, service_name:{service_name}')
    service_timeout = services[service_name]['timeout']
    service_port = services[service_name]['port']
    if action == 'add':
        knocker[ip][service_name] = {}
        knocker[ip][service_name]['timeout'] = service_timeout
        knocker[ip][service_name]['expire_date'] = service_expire_date = datetime.now() + \
            timedelta(seconds=service_timeout)
        return service_name, service_port, service_timeout, service_expire_date
    elif action == 'del':
        knocker[ip].pop(service_name)
        if len(knocker[ip]) == 0:
            knocker.pop(ip)
    elif action == 'update':
        knocker[ip][service_name]['expire_date'] = service_expire_date = datetime.now() + \
            timedelta(seconds=service_timeout)
        return service_name, service_port, service_timeout, service_expire_date


def iptables(action, ip, service_name):
    service_port = services[service_name]['port']
    commands = ''
    for protocol in mode:
        if action == 'add':
            command = f'iptables -I INPUT -p {protocol} -s {ip} --dport {service_port} -j ACCEPT -m comment --comment "webknock: {service_name}, port: {service_port} Allow {ip} access."'
        elif action == 'del':
            command = f'iptables -D INPUT -p {protocol} -s {ip} --dport {service_port} -j ACCEPT -m comment --comment "webknock: {service_name}, port: {service_port} Allow {ip} access."'
        elif action == 'init':
            if system(f'iptables-save | grep "webknock: {service_name}, port: {service_port} Reject all IP access."') == 256:
                command = f'iptables -I INPUT -p {protocol} -s 0.0.0.0/0 --dport {service_port} -j REJECT -m comment --comment "webknock: {service_name}, port: {service_port} Reject all IP access."'
                logging.info('iptables rule does not exist. create rule. iptables 规则不存在，创建规则。')
            else:
                logging.info('iptables rule found. Pass. iptables 规则存在，掠过。')
        logging.info(f'iptables_command: {command}')
        system(command)
        commands = command + ';' + commands
    return commands
