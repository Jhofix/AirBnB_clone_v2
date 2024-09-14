#!/usr/bin/python3
"""SET UP A WEB SERVER
"""
from datetime import datetime
from fabric.api import *
import os.path

env.hosts = ["ubuntu@18.235.233.120"]


def do_deploy(archive_path):
    '''Deploy web_static to web servers

    Args:
        archive_path (str): path to archived file

    Returns:
        False - If any error occurs
        True - If all are successful
    '''
    fname = archive_path.split('/')[-1]
    abs_fname = fpath.split('.')[0]

    try:
        run
        put(f"{archive_path}", f"/tmp/")
        run(f"mkdir -p /data/web_static/releases/{abs_fname}")
        run(f"tar -xvzf /tmp/{fname} -C \
            /data/web_static/releases/{abs_fname}")
        run(f"rm /tmp/{fname}")
        run("rm -r /data/web_static/current")
        run(f"ln -sf /data/web_static/releases/{abs_fname} \
            /data/web_static/current")
    except Exception as e:
        print(f"Error {e}")
        return False
    else:
        return True
