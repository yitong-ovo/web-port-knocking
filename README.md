# web port knocking
先简单的丢一个 Readme，之后再写。

应用场景是这样，

比如你有一个服务(比如ss)，只想知道的人能访问。

那就写个 crontab 去 curl 运行这个服务的服务器，

这样这个端口就会一直对你保持打开，gfw 去扫描的话会被 REJECT(等同这个端口没有打开)。


我还没在 linux 上测试过，不过 iptables 肯定是没问题的。