#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.


import getpass
import os
import socket
import sys
import traceback

import paramiko
from paramiko.py3compat import input

from mobile_robotics_python import Configuration, Console

from . import interactive


class SshConnection:
    def __init__(self, config: Configuration):
        Console.set_logging_file(config.logging_folder)
        Console.info(f"Connecting to {config.remote.ip}")

        # setup logging
        paramiko.util.log_to_file(str(config.logging_folder) + "/paramiko_ssh.log")

        username = config.remote.username
        hostname = config.remote.ip
        port = 22
        password = config.remote.password

        # now connect
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((hostname, port))
        except Exception as e:
            print("*** Connect failed: " + str(e))
            traceback.print_exc()
            sys.exit(1)

        try:
            t = paramiko.Transport(sock)
            try:
                t.start_client()
            except paramiko.SSHException:
                print("*** SSH negotiation failed.")
                sys.exit(1)

            try:
                keys = paramiko.util.load_host_keys(
                    os.path.expanduser("~/.ssh/known_hosts")
                )
            except IOError:
                try:
                    keys = paramiko.util.load_host_keys(
                        os.path.expanduser("~/ssh/known_hosts")
                    )
                except IOError:
                    print("*** Unable to open host keys file")
                    keys = {}

            # check server's host key -- this is important.
            key = t.get_remote_server_key()
            if hostname not in keys:
                print("*** WARNING: Unknown host key!")
            elif key.get_name() not in keys[hostname]:
                print("*** WARNING: Unknown host key!")
            elif keys[hostname][key.get_name()] != key:
                print("*** WARNING: Host key has changed!!!")
                sys.exit(1)
            else:
                print("*** Host key OK.")

            # get username
            if username == "":
                default_username = getpass.getuser()
                username = input("Username [%s]: " % default_username)
                if len(username) == 0:
                    username = default_username

            t.auth_password(username, password)
            chan = t.open_session()
            chan.get_pty()
            chan.invoke_shell()
            print("*** Here we go!\n")
            interactive.interactive_shell(chan)
            chan.close()
            t.close()

        except Exception as e:
            print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
            traceback.print_exc()
            try:
                t.close()
            except Exception:
                pass
            sys.exit(1)
