#!/usr/bin/python3
"""CLEAN UP WEB VERSIONS
"""

from fabric.api import *

def do_clean():
    """Remove older verions of web_static from /data/web_static/releases"""
    run("cd /data/web_static/releases/ && \
        rm -rf $(ls -tr | grep web | tail -n +3)")