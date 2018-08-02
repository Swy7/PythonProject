import os
from datetime import datetime

import paramiko


class SSHServer(object):
    def __init__(self, server_user, server_pwd,
                 server_ip='localhost', server_port=22):
        self.ssh = None
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_user = server_user
        self.server_pwd = server_pwd

    def __enter__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.server_ip, self.server_port, self.server_user, self.server_pwd)
        return self.ssh

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ssh.close()


# 数据库导出
def output_sql(server_user, server_pwd, db_user, db_pwd, db_name, server_ip='localhost',
               server_port=22, output_path=None):
    connection = SSHServer(server_user, server_pwd, server_ip, server_port)
    with connection as f:
        output_filename = db_name + '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.sql'
        if output_path is None:
            output_path = os.path.join(os.getcwd(), 'backup_' + db_name + '_' + datetime.now().strftime('%Y-%m-%d'))
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        os.chdir(output_path)
        db_cmd = 'mysqldump -u {0} -p{1} {2} > {3}'.format(db_user, db_pwd, db_name, output_filename)
        stdin, stdout, stderr = f.exec_command(db_cmd)
    print(stdout.read().decode('utf-8'))
    return stdin, stdout, stderr


# 数据库导入
def input_sql(server_user, server_pwd, db_user, db_pwd, db_name,
              input_file_path, server_ip='localhost', server_port=22):
    if os.path.exists(input_file_path):
        connection = SSHServer(server_user, server_pwd, server_ip, server_port)
        with connection as f:
            input_dir, input_file = os.path.split(input_file_path)
            os.chdir(input_dir)
            db_cmd = 'mysql -u {0} -p{1} {2} < {3}'.format(db_user, db_pwd, db_name, input_file)
            stdin, stdout, stderr = f.exec_command(db_cmd)
        print(stdout.read().decode('utf-8'))
        return stdin, stdout, stderr

    else:
        return '文件不存在'


# 上传文件
def upload_file(server_user, server_pwd, from_path, to_path,
                server_ip='localhost', server_port=22):
    connection = SSHServer(server_user, server_pwd, server_ip, server_port)
    with connection as f:
        sftp = f.open_sftp()
        sftp.put(from_path, to_path)


# 下载文件
def download_file(server_user, server_pwd, from_path, to_path,
                  server_ip='localhost', server_port=22):
    connection = SSHServer(server_user, server_pwd, server_ip, server_port)
    with connection as f:
        sftp = f.open_sftp()
        sftp.get(from_path, to_path)


class ConnectServer(object):
    def __init__(self, server_user, server_pwd,
                 server_ip='localhost', server_port=22):
        self.ssh = None
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_user = server_user
        self.server_pwd = server_pwd

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.server_ip, self.server_port, self.server_user, self.server_pwd)
            return 'ssh connect'
        except Exception as e:
            self.ssh = None
            return ('ssh连接失败 \n', e)

    def close(self):
        if self.ssh:
            self.ssh.close()
            return 'ssh close'
        else:
            return ('未连接ssh')

    # 数据库导出
    def output_sql(self, db_user, db_pwd, db_name, output_path=None):
        if self.ssh:
            output_filename = db_name + '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.sql'
            if output_path is None:
                output_path = os.path.join(os.getcwd(), 'backup_' + db_name + '_' + datetime.now().strftime('%Y-%m-%d'))
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            os.chdir(output_path)
            db_cmd = 'mysqldump -u {0} -p{1} {2} > {3}'.format(db_user, db_pwd, db_name, output_filename)
            stdin, stdout, stderr = self.ssh.exec_command(db_cmd)
            print(stdout.read().decode('utf-8'))
            return stdin, stdout, stderr
        else:
            return ('未连接ssh')

    # 数据库导入
    def input_sql(self, db_user, db_pwd, db_name, input_file_path):
        if self.ssh:
            if os.path.exists(input_file_path):
                input_dir, input_file = os.path.split(input_file_path)
                os.chdir(input_dir)
                db_cmd = 'mysql -u {0} -p{1} {2} < {3}'.format(db_user, db_pwd, db_name, input_file)
                stdin, stdout, stderr = self.ssh.exec_command(db_cmd)
                print(stdout.read().decode('utf-8'))
                return stdin, stdout, stderr
            else:
                return '文件不存在'
        else:
            return ('未连接ssh')

    # 上传文件
    def upload_file(self, from_path, to_path):
        if self.ssh:
            sftp = self.ssh.open_sftp()
            try:
                sftp.put(from_path, to_path)
                return from_path, to_path
            except Exception as e:
                self.close()
                return e
        else:
            return ('未连接ssh')

    # 下载文件
    def download_file(self, from_path, to_path):
        if self.ssh:
            sftp = self.ssh.open_sftp()
            try:
                sftp.get(from_path, to_path)
                return from_path, to_path
            except Exception as e:
                self.close()
                return e
        else:
            return ('未连接ssh')
