#!/usr/bin/python
"""SET UP A WEB SERVER
"""
from datetime import datetime
from fabric.api import *
import os.path

env.hosts = "ubuntu@18.235.233.120"


def do_pack():
    """Archive all files in web_static"""
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path=f"versions/web_static_{time_stamp}.tgz"
    print(path)
    ok = "Good"

    if not os.path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
    if local(f"tar -czvf {path} [0-9]*.py").failed:
        return None
    return os.path.abspath(path)

def do_deploy(archive_path):
    
    fpath = archive_path.split('/')[-1]
    abs_fname = fpath.split('.')[0]
    put_file = "0-setup_web_static.sh"
    '''
    if not os.path.isfile(archive_path):
        print("1_Failed")
        return False
    
    if (put(f"{archive_path}", f"/tmp/{archive_path}").failed):
        return False

    if local(f"tar -xzf {archive_path} -C /data/web_static/releases/{abs_fname}").failed:
        return False
    
    if (run(f"rm /tmp/{archive_path}").failed):
        return False

    if (run(f"ln -sf /data/web_static/releases/{abs_fname} /data/web_static/current").failed):
        return False
    '''
    try:
        put(f"{archive_path}", f"/tmp/{archive_path}")
        local(f"tar -xvzf {archive_path} -C /data/web_static/releases/{abs_fname}")
        run(f"rm /tmp/{archive_path}")
        run(f"ln -sf /data/web_static/releases/{abs_fname} /data/web_static/current")
    except Exception as e:
        print(f"Error {e}")
        return False
    else:
        return True
    
def do_try():
    try:
        local("ls .")
        local('pwd')
        local('ls v*')
    except Exception as e:
        print(f"Error {e}")
        return False
    else:
        return True
    
    #return True