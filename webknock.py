from config import services
from tools import *
from flask import Flask, Response, make_response, request, jsonify
from _thread import start_new_thread
from werkzeug.middleware.proxy_fix import ProxyFix
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
knocker = {}

init_check()

logging.info('init iptables rules. 初始化 iptables 规则。')
for service_name in services:
    iptables('init', None, service_name)

start_new_thread(timeout_check, (knocker,))
@app.route('/<_service_name>/knocking', methods=['GET'])
def knocking(_service_name):
    ip = str(flask_get_ip(request))
    if _service_name in services:
        if ip in knocker and _service_name in knocker[ip]:
            service_name, service_port, service_timeout, service_expire_date, service_last_expire_date = knocker_edit(
                'update', ip, _service_name, knocker)
            command = ''
            message = f'Closing time will be delayed {service_expire_date}.'
            message_zh = f'关门时间将会被延后到 {service_expire_date}。'
        else:
            if ip not in knocker:
                knocker[ip] = {}
            service_name, service_port, service_timeout, service_expire_date, service_last_expire_date = knocker_edit(
                'add', ip, _service_name, knocker)
            command = iptables('add', ip, _service_name)
            message = f'Door opened. Port {service_port} of service {service_name} will be opened for {ip} to {service_expire_date}'
            message_zh = f'门开了， {service_name} 服务的 {service_port} 端口将会为 {ip} 打开到 {service_expire_date}。'

        return_http_code = 200
        return_data = {
            'status': 200,
            'ip': ip,
            'service_name': _service_name,
            'service_timeout': service_timeout,
            'service_port': service_port,
            'expire_date': service_expire_date,
            'last_expire_date': service_last_expire_date,
            'message': message,
            'message_zh': message_zh,
        }
        if logging.DEBUG >= logging.root.level:
            return_data.update({
                'debug': {
                    'command': command,
                    'knocker': knocker
                }
            })
    else:
        return_http_code = 400
        return_data = {
            'status': 400,
            'ip': ip,
            'error_message': 'service name does not exist',
            'error_message_zh': '服务名称不存在。'
        }

    return jsonify(return_data), return_http_code


if __name__ == '__main__':
    app.run(host='0.0.0.0')
