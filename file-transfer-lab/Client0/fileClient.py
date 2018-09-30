#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os


def sendFile(fileName,socket):
    socket.send(b'OK:' + str(os.path.getsize(fileName)).encode())
    with open(fileName, 'rb') as file:
        data = file.read(100)
        sent = socket.send(data)
        while data != b"":
            data = data[sent:]
            data += file.read(100-sent)
            sent = socket.send(data)

server = "127.0.0.1:50000"
debug  = True

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

userInput = input("$ ") # to put file in format "$ put file.txt"
if userInput.startswith("put"):
    fileName = userInput.replace("put ", "")
    s.send(userInput.encode())
    data = s.recv(100).decode()
    if data == 'EXISTS':
        userInput = input("Replace File (Y/N)?")
        if userInput == 'Y':
            sendFile(fileName,s)
        else:
            s.send(b"STOP")
    else:
        sendFile(fileName,s)
