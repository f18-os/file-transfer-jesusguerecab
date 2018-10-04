# Shell Lab

This directory contains:
* python code that implements a server and shell for uploading files to server

Once Server is running the client code asks for an input:
1. It prints "$ "
2. If the user types exit the code stops
3. If the input contains a 'put' it get whatver is after that with a space as a filename
4. If file exsists then it checks if it exists in the server
5. If the file exists in the server it asks if it shopuld be replaced
6. If the file is to be replaced or deosnt exist in server it prepares to recieve the file
7. The file is sent 100 bits at a time till the full file is sent
8. At any moment the server can handle another client connecting

This lab contains the following files
 * Server/fileServer.py: the server code
 * Server/framedSock.py: the code that handles recieving and sending data for server
 * Clien0/fileClient.py: the clients code
 * Client0/framedSock.py: the code that handles recieving and sending data for client (same as server allows for relocation of client0)
 * Client0/file.txt: a text file to test sending
 

To run Server (from \file-transfer-lab\Server\):
~~~
$ ./filServer.py
~~~

To run Client (from \file-transfer-lab\Client0):
~~~
$ ./filClient.py
~~~

What Worked for me from fileClient command line:
~~~
$ put file.txt
$ exit
~~~

# Known Errors #
When Closing client sometimes ends in an error but server keeps runnning
