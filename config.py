'''
# 服务名称，会在请求使用的 url 内出现。
'shadowsocks':{
    'port': 4892, # 服务的端口号，请求之后会开启的端口。
    'timeout' 1800 # 超时时间(秒)，每次触发之后开启多少秒的端口。
}
'''
services = {
    'shadowsocks-1':{
        'port': 4732,
        'timeout': 1800
    },
    'vmess': {
        'port': 4892,
        'timeout': 1800
    }
}

'''
protocol 进行过滤的协议
'''
mode = ['tcp', 'udp']