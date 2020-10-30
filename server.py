#!/usr/bin/python
import socket
import threading

bind_ip = '0.0.0.0'
bind_porta = 22

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_porta))

server.listen(5)

print "Listening on %s:%d" % (bind_ip,bind_porta)



def handler_client(client_socket):
    request = client_socket.recv(1025)
    print "Request: %s" % request
    client_socket.send("HAHA!")
    client_socket.close()



while True:
    client,addr = server.accept()
    print "Accpted %s:%d"%(addr[0],addr[1])

    cliente_handler = threading.Thread(target=handler_client,args=(client,))
    cliente_handler.start()


