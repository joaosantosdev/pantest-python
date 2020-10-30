import socket



client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',21))
client.sendall('Joao')
client.close()