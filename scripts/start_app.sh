#!/usr/bin/bash 
# Change ownership of the project directory
sudo chown -R ubuntu:ubuntu /home/ubuntu/DataScienceDigest-Project
sed -i 's/\[]/\["16.171.176.57"]/' /home/ubuntu/DataScienceDigest-Project/DataScienceDigest/settings.py

python manage.py migrate 
python manage.py makemigrations     
python manage.py collectstatic
sudo certbot --nginx -d datasciencedigest.in -d www.datasciencedigest.in --non-interactive --agree-tos
sudo service gunicorn restart
sudo service nginx restart
#sudo tail -f /var/log/nginx/error.log
#sudo systemctl reload nginx
#sudo tail -f /var/log/nginx/error.log
#sudo nginx -t
#sudo systemctl restart gunicorn
#sudo systemctl status gunicorn
#sudo systemctl status nginx
# Check the status
#systemctl status gunicorn
# Restart:
#systemctl restart gunicorn
#sudo systemctl status nginx
