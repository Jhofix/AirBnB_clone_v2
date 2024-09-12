#!/usr/bin/env bash
# Prepare a web server for deployment

if ! [ -f /usr/sbin/nginx ]; then
    apt-get -y update && apt-get -y update
    apt-get -y install nginx
    ufw allow 'Nginx HTTP'
    echo "Hello World!" > /var/www/html/index.nginx-debian.html
fi

string="\t}\n\
    \n\
    location /hbnb_static {\n\
        alias data/web_static/current/;\n\
    }\n\
    \n\
    if (\$request_filename ~ redirect_me){\n\
        rewrite ^ https://sketchfab.com/bluepeno/models permanent;\n\
    }\n\
    \n\
    add_header X-Served-By $HOSTNAME;\n\
    error_page 404 /error404.html;\n\
    location = /error404.html {\n\
        root /var/www/html;\n\
        internal;\n\
    }"

sed -i "1,/^\t}/ s|^\t}|$string|" /etc/nginx/sites-enabled/default

echo "Ceci n'est pas une page" > /var/www/html/error404.html

mkdir /data/web_static/releases/test/
mkdir /data/web_static/shared/
echo "Ready for web_static deployment" > /data/web_static/releases/test/index.html

if [ -e /data/web_static/current ]; then
    rm /data/web_static/current
else
    ln -s /data/web_static/releases/test/ /data/web_static/current
fi

chown ubuntu /data/

if [ "$(pgrep -c nginx)" -lt 1 ]; then
	service nginx start
else
	service nginx restart
fi