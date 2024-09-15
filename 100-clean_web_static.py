#!/usr/bin/python3
"""CLEAN UP WEB VERSIONS
"""

from fabric.api import *

def do_clean(number=0):
    """Remove older verions of web_static from /data/web_static/releases"""
    n = number
    if number == 0:
        n = 1
    local(f"cd versions && rm -f $(ls -tr | grep web | tail -n +{n + 1})")
    run(f"cd /data/web_static/releases/ && \
        rm -rf $(ls -tr | grep web | tail -n +{n + 1})")