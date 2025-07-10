# 基于Docker挂载VPN

```
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
```

```vim
[Service]
Environment="HTTP_PROXY=http://代理服务器地址:VPN端口"
Environment="HTTPS_PROXY=http://代理服务器地址:VPN端口"
Environment="NO_PROXY=localhost,127.0.0.1,本地网络地址"
```

```
sudo systemctl daemon-reload
sudo systemctl restart docker
```

