# DNSLog
别的轮子实在是用不懂，于是就借鉴+写了个简单的。主要用于漏洞验证。

主要提供以下两个功能：
1. `python manager.py 0.0.0.0:80` 一键部署，包括DNS服务器。因此只需要在申请域名的地方设置好DNS解析路径。
2. 提供`/api/verify?q=域名`接口，如果该`域名`确实被访问过，则返回`{'data': 'Yes'}`，否则返回`{'data': 'No'}`
3. 提供`JWTToken` 认证，只允许认证的人使用`/api/verify?q=域名`接口

4. **记得修改`logger.py`和`scripts/logger.py`中的主机IP，修改为 `dnslog主机IP`**

## 部署步骤
两种部署方案：一种是直接裸奔上 `python manager.py makemigrations`, `python manager.py migrate`, `python manager.py 0.0.0.0:80`，坏处是静态文件找不到，admin界面难看；另一种则是通过Apache部署，这里直接介绍第二种。

部署主机是在Ubuntu 18上：
1. 安装apache2以及相关组件：`apt-get install apache2 libapache2-mod-wsgi-py3`
2. 安装virtualenv：`pip3 install virtualenv`
3. 将改项目放在 `/var/www` 下
4. 在`/var/www/dnslog` 下运行 `virtualenv env`，并运行 `source /var/www/dnslog/env/bin/activate`
5. 在`/var/www/dnslog/dnslog` 下运行 `pip install -r req.tt`
6. 修改`/var/www/dnslog/dnslog/dnslog/setting.py` 中的 `ALLOWED_HOSTS = []` 改为 `ALLOWED_HOSTS = ['dnslog主机IP']`，以及`DEBUG=True`改为`DEBUG=False`
7. 配置apache， `vim /etc/apache2/sites-avaliable/000-default.conf` 添加如下行：
```
<VirtualHost *:80>
        Alias /static /var/www/dnslog/dnslog/dnslog/static
        <Directory /var/www/dnslog/dnslog/dnslog/static>
                Require all granted
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
        WSGIScriptAlias / /var/www/dnslog/dnslog/dnslog/wsgi.py
        WSGIDaemonProcess dnslog python-path=/var/www/dnslog/dnslog/ python-home=/var/www/dnslog/env
        WSGIProcessGroup dnslog
        WSGIPassAuthorization On
        <Directory /var/www/dnslog/dnslog/dnslog>
        <Files wsgi.py>
                Require all granted
        </Files>
        </Directory>
</VirtualHost>
```
8. 运行`python manager.py makemigrations`, `python manager.py migrate`, `python manager.py collectstatic`
9. 运行 `chown -R www-data:www-data /var/www/dnslog` 
10. 运行`service apache start`
11. 由于apache是www-data权限，无法绑定端口，手动运行`nohup python manager.py runscript logger`开启dns记录
10. 搞定

## 关于DNS解析的配置
我是在阿里云上整的。所以这里只提供阿里云的配置方法。

	1. 在阿里云上买个域名。
	2. 在 `云解析DNS/域名解析/解析设置 `里面设置两个记录
		2.1、ns	A `你的dnslog主机IP`
		2.2、\*	A `你的dnslog主机IP`
	3. 在 `自定义DNS Host`中设置你的 `dnslog主机IP`
	4. 在 `DNS修改` 中添加两条DNS解析路径，第一个用你的`dnslog主机IP`，第二个选个能用的就行。
	5. 以上四步就搞定了。

## 使用步骤
1. 运行 `python manager.py createsuperuser` 新建一个账户。
2. 从 `api/user/login` 处登录获取`JWTToken`，Token有效期无限
3. 在header中加一个`Authorization: JWT xxxxx`，其中`xxxxx`为第二步获得的token，访问`/api/verify?q=域名`获知靶机是否执行命令。

PS：如果是想利用DNSLog带数据出来，可以在`admin/`，利用新建的账户登录，在`dns log`标签下就是近期所有的dns请求列表。
