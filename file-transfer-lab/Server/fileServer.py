#! /usr/bin/env python3

import sys, os
import re, socket

def recieveFile(fileName,lsocket, fileSize):
    file = open(fileName, 'wb')
    data = lsocket.recv(100)
    size = len(data)
    file.write(data)
    while size < int(fileSize):
        data = s.recv(100)
        size += len(data)
        file.write(data)
    print("Download Complete!")

debug = True
listenPort = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener lsocket
bindAddr = ("127.0.0.1", listenPort)
s.bind(bindAddr)
s.listen(5)
print("listening on:", bindAddr)

sock, addr = s.accept()
print("connection rec'd from", addr)

while True:
    payload = sock.recv(100).decode()
    if payload[:3] == "put":
        fileName = payload.replace("put ", "")
        if os.path.isfile(fileName):
            sock.send(b'EXISTS')
            payload = sock.recv(100).decode()
            if payload[:3] == 'OK:':
                recieveFile(fileName,sock,payload[3:])
        else:
            sock.send(b'NO')
            payload = sock.recv(100).decode()
            recieveFile(fileName,sock,payload[3:])
    if not payload:
        break
    payload += "!"
