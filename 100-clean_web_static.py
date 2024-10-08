#!/usr/bin/python3
"""CLEAN UP WEB VERSIONS
"""

from fabric.api import *
env.hosts = ["18.235.233.120", "54.242.193.230"]


def do_clean(number=0):
    """Remove older verions of web_static from /data/web_static/releases"""
    n = int(number)
    if number == 0:
        n = 1
    local(f"cd versions && rm -f $(ls -tr | grep web | tail -n +{n + 1})")
    run(f"cd /data/web_static/releases/ && \
        rm -rf $(ls -tr | grep web | tail -n +{n + 1})")
