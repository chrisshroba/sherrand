#!/usr/bin/env bash
echo "Provisioning Sherrand box..."

cd /vagrant

sudo apt-get update

# Install Nginx
sudo apt-get install nginx -y

# Install python components 
sudo apt-get install python-pip python-dev libmysqlclient-dev build-essential -y
sudo pip install virtualenv

# Install MySQL
# Need to pre-set the password so that it installs property
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password password'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password password'
sudo apt-get install mysql-server -y

mysql -u "root" "-ppassword" < "vagrant/setup.sql"

# Create and activate virtualenv
virtualenv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install and configure uWSGI and Nginx
sudo apt-get install uwsgi uwsgi-plugin-python -y

sudo ln -s /vagrant/vagrant/sherrand.ini /etc/uwsgi/apps-enabled/sherrand.ini

sudo service uwsgi restart

sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/default

sudo ln -s /vagrant/vagrant/sherrand.conf /etc/nginx/sites-enabled/

sudo service nginx restart
