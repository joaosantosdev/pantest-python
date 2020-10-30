#!/usr/bin/python

import sys
import socket
import getopt
import threading
import subprocess
import os
import json

from const import execute,upload_destination,upload,command,target,port,listen,Example


def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except Exception as e:
        output = "Failed: "+str(e)
    return output


def client_sender(buffer):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
        data_len = 1
        response = ''
        while "sair" not in response:
            data = client.recv(4096)
            print data
            buffer = raw_input("")
            buffer += '\n'
            client.send(buffer)
            response = data
        print response


    except Exception as e:
        print 'Exception! Exiting...'
        client.close()

def client_handler(client_socket,data):
    global upload,execute,command
    if len(upload_destination):
        try:
            file_descriptor = open(upload_destination,'wb')
            file_descriptor.write(data['message'])
            file_descriptor.close()
            client_socket.send("Successfully saved file to %s\r\n !"%upload_destination)
        except:
            client_socket.send("Failed to save file to  %s\r\n !"%upload_destination)

    if len(execute):
        print "Excute"
        output = run_command(execute)
        client_socket.send(output)

    if command:
        client_socket.send("<--# Command #-->")
        print 'cmd_buffer'
        while True:
            cmd_buffer = client_socket.recv(1024)
            print cmd_buffer.rstrip() == ':x'
            print cmd_buffer.rstrip()  +"=="+':x'
            if cmd_buffer.rstrip() == ':x':
                break
            client_socket.send("<--# Command #-->\n"+run_command(cmd_buffer))

def server_loop():
    global target,execute,command,upload_destination,upload

    if not len(target):
        target = '0.0.0.0'

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    print "Server run  %s:%s" %(target,port)
    while True:
        client_socket,addr = server.accept()
        file_buffer = client_socket.recv(1024)

        print "file"+str(file_buffer)
        data = json.loads(file_buffer)
        command = data['command']
        execute = data['execute']
        upload = data['upload']
        upload_destination = data['upload_destination']
        client_thread = threading.Thread(target=client_handler,args=[client_socket,data,])
        client_thread.start()



def main():
    global listen
    global port,execute,command,upload_destination,target
# if not len(sys.argv[1:]):
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu",["help","listen","execute","target","port","command","upload"])
        for o,a in opts:
            if o in ("-h", "--help"):
                print
            elif o in ("-l", "--listen"):
                listen = True
            elif o in ("-e", "--execute"):
                execute = a
            elif o in ("-c", "--commandshell"):
                command = True
            elif o in ("-u", "--upload"):
                upload_destination = a
            elif o in ("-t", "--target"):
                target = a
            elif o in ("-p", "--port"):
                print("port")
                port = int(a)
            else:
                assert False, 'Unhandled Option'

        if not listen and len(target) and port > 0:
            buffer = sys.stdin.read()
            jsonData = {
                'message':buffer,
                'execute':execute,
                'command':command,
                'upload':upload,
                'upload_destination':upload_destination
            }
            print "Sen der"
            client_sender(json.dumps(jsonData))

        if listen:
            server_loop()
    except getopt.GetoptError as e:
        print("Erro",e)



main()

