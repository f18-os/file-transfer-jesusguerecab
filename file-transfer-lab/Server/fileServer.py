#! /usr/bin/env python3

import sys, os
import re, socket

from framedSock import framedSend, framedReceive

def recieveFile(fileName,lsocket, fileSize):
    file = open(fileName, 'wb')
    #data = lsocket.recv(100)
    data = framedReceive(lsocket, debug)
    size = len(data)
    file.write(data)
    while size < int(fileSize):
        data = framedReceive(lsocket, debug)
        #data = s.recv(100)
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

while True:
    sock, addr = s.accept()
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc != 0: #Parent goes to next iteration
        continue
    #Child handles current connection
    print("connection rec'd from", addr)
    while True:
        payload = framedReceive(sock, debug)
        if payload is not None:
            payload = payload.decode()
            if payload[:3] == "put":
                fileName = payload.replace("put ", "")
                if os.path.isfile(fileName):
                    framedSend(sock, b'EXISTS', debug)
                    payload = framedReceive(sock, debug).decode()
                    if payload[:3] == 'OK:':
                        recieveFile(fileName,sock,payload[3:])
                else:
                    framedSend(sock, b'NO', debug)
                    payload = framedReceive(sock, debug).decode()
                    recieveFile(fileName,sock,payload[3:])
        if not payload:
            break
