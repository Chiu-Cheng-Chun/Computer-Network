# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:58:18 2018

@author: craig
"""

import socket, sys

def main():
    if len(sys.argv) <= 1:
        print('Usage : "python ProxyServer.py server_ip"\n server_ip : It is the IP Address Of Proxy Server')
        sys.exit(2)
    # Create a server socket, bind it to a port and start listening
    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSerPort = 8888
    tcpSerSock.bind(("", tcpSerPort))
    tcpSerSock.listen(5)
    
    while True:
        print('Ready to serve...')
        tcpCliSock, addr = tcpSerSock.accept()# Strat receiving data from the client
        print('Received a connection from:', addr)
        message = tcpCliSock.recv(1024)
        print(message)
        print(message.split()) # Extract the filename from the given message
        filename = "www.google.com"
        fileExist = "false"
        filetouse = "/" + filename
        print(filetouse)
        try:
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "rb")
            outputdata = f.readlines()
            fileExist = "true"
            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n".encode())
            for i in range(len(outputdata)):
                tcpCliSock.send(outputdata[i])
            print('Read from cache')
            # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxyserver
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:           
                    c.connect(("google.com", 80))# Connect to the socket to port 80 
                    fileobj = c.makefile('rwb', 0)# Create a temporary file on this socket and ask port 80 for the file requested by the client
                    fileobj.write("GET https://www.google.com HTTP/1.0\n\n".encode())
                    # Read the response into buffer
                    buff = fileobj.readlines()
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile = open("./www.google.com".encode(),"wb")
                    for i in range(0, len(buff)):
                        tmpFile.write(buff[i])
                    tcpCliSock.send(buff[i])
                except FileNotFoundError:
                    print("Illegal request")
            else:
                # HTTP response message for file not found
                print("404 Error file not found.")
            # Close the client and the server sockets
            tcpCliSock.close()
        
if __name__ == '__main__':
    main()
