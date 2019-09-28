# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:58:18 2018

@author: craig
"""

import socket, sys
from urllib.request import Request, urlopen, HTTPError

def fetch_file(filename):
    # Let's try to read the file locally first
    file_from_cache = fetch_from_cache(filename)

    if file_from_cache:
        print('Fetched successfully from cache.')
        return file_from_cache
    else:
        print('Not in cache. Fetching from server.')
        file_from_server = fetch_from_server(filename)

        if file_from_server:
            save_in_cache(filename, file_from_server)
            return file_from_server
        else:
            return None


def fetch_from_cache(filename):
    try:
        # Check if we have this file locally
        fin = open('cache' + filename)
        content = fin.read()
        fin.close()
        # If we have it, let's send it
        return content
    except IOError:
        return None


def fetch_from_server(filename):
    url = 'http://192.168.1.101:8888/' + filename
    q = Request(url)
    try:
        response = urlopen(q)
        # Grab the header and content from the server req
        content = response.read().decode('utf-8')
        return content
    except HTTPError:
        return None


def save_in_cache(filename, content):
    print('Saving a copy of {} in the cache'.format(filename))
    cached_file = open('cache' + filename, 'w')
    cached_file.write(content)
    cached_file.close()


def main():
    if len(sys.argv) <= 1:
        print('Usage : "python ProxyServer.py server_ip"\n server_ip : It is the IP Address Of Proxy Server')
        sys.exit(2)
    # Create a server socket, bind it to a port and start listening
    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSerPort = 8888
    tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #for cacheproxy
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
            content = fetch_file(filename)
            if content:
                response = 'HTTP/1.0 200 OK\r\n' + content
            else:
                response = 'HTTP/1.0 404 NOT FOUND\r\n File Not Found'
            tcpCliSock.send(response.encode())
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "rb")
            outputdata = f.readlines()
            fileExist = "true"
           
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
                    """
                    fileobj.write("GET https://www.google.com HTTP/1.0\n\n".encode())
                    """
                    fileobj.write("POST https://www.google.com HTTP/1.0\n\n".encode())
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
                tcpCliSock.send("404 Error file not found.".encode())
            # Close the client and the server sockets
            tcpCliSock.close()
        
if __name__ == '__main__':
    main()
