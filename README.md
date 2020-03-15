# web port knocking
简单的 port knocking 实现，使用 web requests 请求来让 iptables 开启端口。

推荐设置反向代理以使用 https 进行请求。

用起来很简单:
```bash
$ curl http://localhost:5000/shadowsocks/knocking | jq
```
```json
{
  "expire_date": "Sun, 15 Mar 2020 14:34:22 GMT",
  "message": "Door opened. Port 4892 of service shadowsocks will be opened for 10.0.0.247 to 2020-03-15 14:34:22.685407",
  "message_zh": "门开了， vmess 服务的 4892 端口将会为 10.0.0.247 打开到 2020-03-15 14:34:22.685407。",
  "service_name": "shadowsocks",
  "service_port": 4892,
  "service_timeout": 1800,
  "status": 200
}
```
上述的 URL 中，`shadowsocks` 是服务名。进行请求之后，程序会调用 `iptables` 允许发出请求的 IP 访问请求相应服务的端口。

在过期时间之前使用相同 IP 再次对 URL 进行请求，程序会延长过期时间。
```bash
$ curl http://localhost:5000/shadowsocks/knocking | jq
```
```json
{
  "expire_date": "Sun, 15 Mar 2020 14:41:46 GMT",
  "message": "Closing time will be delayed 2020-03-15 14:41:46.389120.",
  "message_zh": "关门时间将会被延后到 2020-03-15 14:41:46.389120。",
  "service_name": "shadowsocks",
  "service_port": 4892,
  "service_timeout": 1800,
  "status": 200
}
```

## 配置
在 [config.py](config.py) 进行配置。目前有两个配置项: `services`, `protocol`。

可以参考预置的配置作为示例。