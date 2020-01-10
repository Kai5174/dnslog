# DNSLog
�������ʵ�����ò��������Ǿͽ��+д�˸��򵥵ġ���Ҫ����©����֤��

��Ҫ�ṩ�����������ܣ�
1. `python manager.py 0.0.0.0:80` һ�����𣬰���DNS�����������ֻ��Ҫ�����������ĵط����ú�DNS����·����
2. �ṩ`/api/verify?q=����`�ӿڣ������`����`ȷʵ�����ʹ����򷵻�`{'data': 'Yes'}`�����򷵻�`{'data': 'No'}`
3. �ṩ`JWTToken` ��֤��ֻ������֤����ʹ��`/api/verify?q=����`�ӿ�

4. **�ǵ��޸�`logger.py`��`scripts/logger.py`�е�����IP���޸�Ϊ `dnslog����IP`**

## ������
���ֲ��𷽰���һ����ֱ���㱼�� `python manager.py makemigrations`, `python manager.py migrate`, `python manager.py 0.0.0.0:80`�������Ǿ�̬�ļ��Ҳ�����admin�����ѿ�����һ������ͨ��Apache��������ֱ�ӽ��ܵڶ��֡�

������������Ubuntu 18�ϣ�
1. ��װapache2�Լ���������`apt-get install apache2 libapache2-mod-wsgi-py3`
2. ��װvirtualenv��`pip3 install virtualenv`
3. ������Ŀ���� `/var/www` ��
4. ��`/var/www/dnslog` ������ `virtualenv env`�������� `source /var/www/dnslog/env/bin/activate`
5. ��`/var/www/dnslog/dnslog` ������ `pip install -r req.tt`
6. �޸�`/var/www/dnslog/dnslog/dnslog/setting.py` �е� `ALLOWED_HOSTS = []` ��Ϊ `ALLOWED_HOSTS = ['dnslog����IP']`���Լ�`DEBUG=True`��Ϊ`DEBUG=False`
7. ����apache�� `vim /etc/apache2/sites-avaliable/000-default.conf` ��������У�
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
8. ����`python manager.py makemigrations`, `python manager.py migrate`, `python manager.py collectstatic`
9. ���� `chown -R www-data:www-data /var/www/dnslog` 
10. ����`service apache start`
11. ����apache��www-dataȨ�ޣ��޷��󶨶˿ڣ��ֶ�����`nohup python manager.py runscript logger`����dns��¼
10. �㶨

## ����DNS����������
�����ڰ����������ġ���������ֻ�ṩ�����Ƶ����÷�����

	1. �ڰ����������������
	2. �� `�ƽ���DNS/��������/�������� `��������������¼
		2.1��ns	A `���dnslog����IP`
		2.2��\*	A `���dnslog����IP`
	3. �� `�Զ���DNS Host`��������� `dnslog����IP`
	4. �� `DNS�޸�` ���������DNS����·������һ�������`dnslog����IP`���ڶ���ѡ�����õľ��С�
	5. �����Ĳ��͸㶨�ˡ�

## ʹ�ò���
1. ���� `python manager.py createsuperuser` �½�һ���˻���
2. �� `api/user/login` ����¼��ȡ`JWTToken`��Token��Ч������
3. ��header�м�һ��`Authorization: JWT xxxxx`������`xxxxx`Ϊ�ڶ�����õ�token������`/api/verify?q=����`��֪�л��Ƿ�ִ�����

PS�������������DNSLog�����ݳ�����������`admin/`�������½����˻���¼����`dns log`��ǩ�¾��ǽ������е�dns�����б�
