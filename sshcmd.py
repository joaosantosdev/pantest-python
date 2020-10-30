#!/usr/bin/python
import threading
import os
import paramiko
import subprocess


def ssh_command(ip,user,passwd,command):
    cliente = paramiko.SSHClient()
    #cliente.load_host_keys('/home/joaosantosdev/.ssh/known_hosts')
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cliente.connect(ip,username=user,password=passwd)
    ssh_session = cliente.get_transport().open_session()
    if(ssh_session.active):
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))
    return

ssh_command('127.0.0.1','joaosantosdev','ltj120116','ClientConnected')