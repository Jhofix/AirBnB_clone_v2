"""SET UP A WEB SERVER
"""
from datetime import datetime
from fabric.api import *
import os.path


def do_pack():
    """Archive all files in web_static"""
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path=f"versions/web_static_{time_stamp}.tar"
    print(path)
    ok = "Good"

    if not os.path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
    if local(f"tar -cvf {path} web_static").failed:
        return None
    return os.path.abspath(path)
