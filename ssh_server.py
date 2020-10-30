#!/usr/bin/python
import subprocess
import paramiko
import os
import threading
import sys
import socket

host_key = paramiko.RSAKey(filename='id_rsa_server')

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self,kind,chanid):
        print(kind)
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


    def check_auth_password(self, username, password):
        if(username == 'joaosantosdev' and password == 'ltj120116'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]
port = int(sys.argv[2])

try:

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Para dizer que 'e umm socket SSH
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind((server,port))
    sock.listen(100)
    print("[*] Listener for connection...")
    client,addr = sock.accept()
except Exception,e:
    print("[-] Listener failed: "+str(e))
    sys.exit(0)
print ('[+] Got a connection !')


try:
    session = paramiko.Transport(client)
    session.add_server_key(host_key)
    server = Server()
    try:
        session.start_server(server=server)
    except paramiko.SSHException as e:
        print("[-] SSH negotiation failed")
    chan = session.accept(20)
    print('[+] Autheticated')
    print(chan.recv(1024))
    chan.send('Welcome to ssh')

    while True:
        try:
            command = raw_input('Enter command: ').strip('\n')
            if command != 'exit':
                chan.send(command)
                print(chan.recv(1024)+'\n')
            else:
                chan.send('exit')
                print('Exiting ...')
                session.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            session.close()
except Exception,e:
    print('[-] Caught exception: '+str(e))
    try:
        session.close()
    except:
        pass
    sys.exit(0)