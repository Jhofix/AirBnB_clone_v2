#!/usr/bin/env bash
# Prepare a web server for deployment

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
