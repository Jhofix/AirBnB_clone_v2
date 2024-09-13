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
    fpath = archive_path.split('/')[-1]
    abs_fname = fpath.split('.')[0]

    try:
        put(f"{archive_path}", f"/tmp/{archive_path}")
        local(f"tar -xvzf {archive_path} -C \
              /data/web_static/releases/{abs_fname}")
        run(f"rm /tmp/{archive_path}")
        run(f"ln -sf /data/web_static/releases/{abs_fname} \
            /data/web_static/current")
    except Exception as e:
        print(f"Error {e}")
        return False
    else:
        return True
