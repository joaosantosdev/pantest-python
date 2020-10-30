
print()
'''
#!/usr/bin/python
import threading
import os
import subprocess
import paramiko
import subprocess



def ssh_command(ip,user,passwd,command):
    cliente = paramiko.SSHClient()
  #  cliente.load_host_keys('id_rsa')
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cliente.connect(ip,username=user,password=passwd)

    ssh_session = cliente.get_transport().open_session()
    if(ssh_session.active):
        ssh_session.send(command)
        print(ssh_session.recv(1024))
        while True:
            command = ssh_session.recv(1024)
            try:
                print('Command: '+command)
                cmd_output = subprocess.call(command,shell=True)
                print('Output: '+str(cmd_output))
                if cmd_output == '':
                    cmd_output = 'Without return'
                ssh_session.send(str(cmd_output))
            except Exception,e:
                print 'erro'
                ssh_session.send(str(e))
        ssh_session.close()
    return

ssh_command('127.0.0.1','joaosantosdev','ltj120116','ClientConnected')
'''