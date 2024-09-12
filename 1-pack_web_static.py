#!/usr/bin/python3
"""SET UP A WEB SERVER
"""
from datetime import datetime
from fabric.api import *
import os.path


def do_pack():
    """Archive all files in web_static"""
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")

    if not os.path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
        else:
            print("SUCCEESSFUL: Created directory(s) successfully")

    if os.path.isdir("versions"):
        if not local("tar -cvf versions/web_static_{}.tar *"
                     .format(time_stamp)):
            return None
