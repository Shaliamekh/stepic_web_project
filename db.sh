sudo /etc/init.d/mysql start
mysql -u root -e "create database stepic_web;"
mysql -u root -e "grant all privileges on stepic_web.* to 'box'@'localhost' with grant option;"
~/web/ask/manage.py makemigrations
~/web/ask/manage.py migrate