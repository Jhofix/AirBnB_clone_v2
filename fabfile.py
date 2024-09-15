#!/usr/bin/python3
"""SET UP A WEB SERVER
"""
from datetime import datetime
from fabric.api import *
import os.path

env.hosts = ["ubuntu@18.235.233.120", "ubuntu@54.242.193.230"]

run_time = lambda : datetime.now().strftime("%Y%m%d%H%M%S")
time_stamp = run_time()

def do_pack():
    """Archive all files in web_static"""
    #time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    #run_time = lambda : datetime.now().strftime("%Y%m%d%H%M%S")
    #time_stamp = run_time()
    path = f"versions/web_static_{time_stamp}.tgz"
    target = f"web_static"

    if not os.path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
    if local(f"tar -czvf {path} {target}").failed:
        return None
    return os.path.abspath(path)


def do_deploy(archive_path):
    """Deploy to web servers"""
    fname = archive_path.split('/')[-1]
    abs_fname = fname.split('.')[0]

    try:
        put(f"{archive_path}", f"/tmp/")
        run(f"mkdir -p /data/web_static/releases/{abs_fname}")
        run(f"tar -xvzf /tmp/{fname} -C \
            /data/web_static/releases/{abs_fname} --strip-components=1")
        run(f"rm /tmp/{fname}")
        run("rm -r /data/web_static/current")
        run(f"ln -s /data/web_static/releases/{abs_fname} \
            /data/web_static/current")
    except Exception as e:
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


def deploy():
    """Archives and deploy web_static to servers"""
    fpack = do_pack()
    print(fpack)
    if (fpack is None):
        return False
    return do_deploy(fpack)

def do_clean(number=0):
    """Remove older verions of web_static from /data/web_static/releases"""
    n = int(number)
    if number == 0:
        n = 1
    local(f"cd versions && rm -f $(ls -tr | grep web | tail -n +{n + 1})")
    run(f"cd /data/web_static/releases/ && \
        rm -rf $(ls -tr | grep web | tail -n +{n + 1})")