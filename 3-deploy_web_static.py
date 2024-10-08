#!/usr/bin/python3
"""SET UP A WEB SERVER
"""
from datetime import datetime
from fabric.api import *
import os.path

env.hosts = ["18.235.233.120", "54.242.193.230"]


def do_pack():
    """Archive all files in web_static"""
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path = f"versions/web_static_{time_stamp}.tgz"
    target = f"web_static"

    if not os.path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
    if local(f"tar -czvf {path} {target}").failed:
        return None
    return os.path.abspath(path)


def do_deploy(archive_path):

    fname = archive_path.split('/')[-1]
    abs_fname = fname.split('.')[0]

    try:
        run
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


def deploy():
    """Archives and deploy web_static to servers"""
    fpack = do_pack()
    if (fpack is None):
        return False
    return do_deploy(fpack)
