#!/usr/bin/env bash
# Prepare a web server for deployment

if ! [ -f /usr/sbin/nginx ]; then
    apt-get -y update
    apt-get -y install nginx
    ufw allow 'Nginx HTTP'
    echo "Hello World!" > /var/www/html/index.nginx-debian.html
    service nginx start
fi

string="\tif (\$request_filename ~ redirect_me){\
		\n\t\trewrite ^ https://sketchfab.com/bluepeno/models permanent;\
	\n\t}\n\
    \n\tadd_header X-Served-By $HOSTNAME;\
	\n\terror_page 404 /error404.html;\
	\n\tlocation = /error404.html {\
		\n\t\troot /var/www/html;\
		\n\t\tinternal;\
	\n\t}"

echo "Ceci n'est pas une page" > /var/www/html/error404.html
sed -i "53 i\ $string" /etc/nginx/sites-enabled/default

if [ "$(pgrep -c nginx)" -lt 1 ]; then
	service nginx start
else
	service nginx restart
fi

if ! [ -e /data/ ]; then
    mkdir /data/

    if ! [ -e /data/web_static/ ]; then
        mkdir /data/web_static/
    fi

    if ! [ -e /data/web_static/releases/ ]; then
        mkdir /data/web_static/releases/
    fi

    if ! [ -e /data/web_static/shared/ ]; then
        mkdir /data/web_static/shared/
    fi

    if ! [ -e /data/web_static/releases/test/ ]; then
        mkdir /data/web_static/releases/test/
    fi
fi

echo "Ready for web_static deployment" > /data/web_static/releases/test/index.html

if [ -e /data/web_static/current ]; then
    rm /data/web_static/current
else
    ln -s /data/web_static/releases/test/ /data/web_static/current
fi

chown ubuntu:ubuntu /data/
alias="\t}\n\
    location \/hbnb_static {\n\
        alias data\/web_static\/current\/;\n\
    }\n"

sed "1,/^\t}/ s/^\t}/$alias/" /etc/nginx/sites-enabled/efault

sudo service nginx restart
