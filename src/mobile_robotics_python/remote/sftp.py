import os
import socket
from stat import S_ISDIR

import paramiko

from mobile_robotics_python import Configuration, Console


class SSHSession(object):
    # Usage:
    # Detects DSA or RSA from key_file, either as a string filename or a
    # file object.  Password auth is possible, but I will judge you for
    # using it. So:
    # ssh=SSHSession('targetserver.com','root',key_file=open('mykey.pem','r'))
    # ssh=SSHSession('targetserver.com','root',key_file='/home/me/mykey.pem')
    # ssh=SSHSession('targetserver.com','root','mypassword')
    # ssh.put('filename','/remote/file/destination/path')
    # ssh.put_all('/path/to/local/source/dir','/path/to/remote/destination')
    # ssh.get_all('/path/to/remote/source/dir','/path/to/local/destination')
    # ssh.command('echo "Command to execute"')

    def __init__(self, hostname, username="root", key_file=None, password=None):
        #
        #  Accepts a file-like object (anything with a readlines() function)
        #  in either dss_key or rsa_key with a private key.  Since I don't
        #  ever intend to leave a server open to a password auth.
        #
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, 22))
        self.t = paramiko.Transport(self.sock)
        self.t.start_client()
        key = self.t.get_remote_server_key()
        # supposed to check for key in keys, but I don't much care right now to find the right notation
        if key_file is not None:
            if isinstance(key, str):
                key_file = open(key, "r")
            key_head = key_file.readline()
            key_file.seek(0)
            if "DSA" in key_head:
                keytype = paramiko.DSSKey
            elif "RSA" in key_head:
                keytype = paramiko.RSAKey
            else:
                raise Exception("Can't identify key type")
            pkey = keytype.from_private_key(key_file)
            self.t.auth_publickey(username, pkey)
        else:
            if password is not None:
                self.t.auth_password(username, password, fallback=False)
            else:
                raise Exception("Must supply either key_file or password")
        self.sftp = paramiko.SFTPClient.from_transport(self.t)

    def command(self, cmd):
        #  Breaks the command by lines, sends and receives
        #  each line and its output separately
        #
        #  Returns the server response text as a string

        chan = self.t.open_session()
        chan.get_pty()
        chan.invoke_shell()
        chan.settimeout(20.0)
        ret = ""
        try:
            ret += chan.recv(1024)
        except socket.timeout:
            chan.send("\n")
            ret += chan.recv(1024)
        for line in cmd.split("\n"):
            chan.send(line.strip() + "\n")
            ret += chan.recv(1024)
        return ret

    def put(self, localfile, remotefile):
        #  Copy localfile to remotefile, overwriting or creating as needed.
        self.sftp.put(localfile, remotefile)

    def put_all(self, localpath, remotepath):
        #  recursively upload a full directory
        os.chdir(os.path.split(localpath)[0])
        parent = os.path.split(localpath)[1]
        base = os.path.split(localpath)[0]
        for walker in os.walk(parent):
            try:
                self.sftp.mkdir(os.path.join(remotepath, walker[0]))
            except IOError:
                pass
            for file in walker[2]:
                if (
                    "logs" in walker[0]
                    or ".git" in walker[0]
                    or "__pycache__" in walker[0]
                    or ".pyc" in file
                    or ".egg-info" in walker[0]
                ):
                    continue
                srcfile = os.path.join(base, walker[0], file)
                dstfile = os.path.join(remotepath, walker[0], file)
                print("Uploading %s" % (file))
                self.put(
                    srcfile,
                    dstfile,
                )

    def get(self, remotefile, localfile):
        #  Copy remotefile to localfile, overwriting or creating as needed.
        self.sftp.get(remotefile, localfile)

    def sftp_walk(self, remotepath):
        # Kindof a stripped down  version of os.walk, implemented for
        # sftp.  Tried running it flat without the yields, but it really
        # chokes on big directories.
        path = remotepath
        files = []
        folders = []
        for f in self.sftp.listdir_attr(remotepath):
            if S_ISDIR(f.st_mode):
                folders.append(f.filename)
            else:
                files.append(f.filename)
        print(path, folders, files)
        yield path, folders, files
        for folder in folders:
            new_path = os.path.join(remotepath, folder)
            for x in self.sftp_walk(new_path):
                yield x

    def get_all(self, remotepath, localpath):
        #  recursively download a full directory
        #  Harder than it sounded at first, since paramiko won't walk
        #
        # For the record, something like this would gennerally be faster:
        # ssh user@host 'tar -cz /source/folder' | tar -xz

        self.sftp.chdir(os.path.split(remotepath)[0])
        parent = os.path.split(remotepath)[1]
        try:
            os.mkdir(localpath)
        except OSError:
            pass
        for walker in self.sftp_walk(parent):
            try:
                os.mkdir(os.path.join(localpath, walker[0]))
            except OSError:
                pass
            for file in walker[2]:
                self.get(
                    os.path.join(walker[0], file),
                    os.path.join(localpath, walker[0], file),
                )

    def write_command(self, text, remotefile):
        #  Writes text to remotefile, and makes remotefile executable.
        #  This is perhaps a bit niche, but I was thinking I needed it.
        #  For the record, I was incorrect.
        self.sftp.open(remotefile, "w").write(text)
        self.sftp.chmod(remotefile, 755)


class SftpConnection:
    def __init__(self, config: Configuration, source_directory: str):
        Console.set_logging_file(config.logging_folder)
        Console.info(f"Connecting to {config.remote.ip}")

        # setup logging
        paramiko.util.log_to_file(str(config.logging_folder) + "/paramiko_sftp.log")

        username = config.remote.username
        hostname = config.remote.ip
        password = config.remote.password
        target_directory = config.remote.upload_destination

        print(
            "Uploading the directory '%s' to '%s'"
            % (source_directory, target_directory),
            "at",
            hostname,
        )

        ssh = SSHSession(hostname, username, password=password)
        ssh.put_all(source_directory, target_directory)
