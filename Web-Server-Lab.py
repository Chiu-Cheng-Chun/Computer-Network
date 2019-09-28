# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 20:51:55 2018

@author: craig
"""

#import socket module
from socket import *
import sys # In order to terminate the program
import time

#Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM) # setup socket server
host = '' #預設localhost
Port = 8087 #port_number
max_queued = 1 #最大等待要求數
buffer_size = 3000 #buffer的size
serverSocket.bind((host,Port))
serverSocket.listen(max_queued)
print('Server is now listening on port "', Port,'"') #開始監聽此port

while True:
     #Establish the connection
     print('Ready to serve...')
     connectionSocket, addr = serverSocket.accept() # 允許連接
     try:
         message = connectionSocket.recv(buffer_size) # get request and filename
         filename = message.split()[1]
         f = open(filename[1:]) # open requested file
         outputdata = f.read() # read file and close
         f.close()
         
         #Send one HTTP header line into socket
         connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode()) # 傳送HTTP狀態
         lastModifiedTime = time.strftime('%a %b %d %H:%M:%S %Y')
         connectionSocket.send('Last-Modified: {0}\r\n'.encode())
         connectionSocket.send("Content-Type: text/html\r\n\r\n".encode()) # send content type to client
         
         #Send the content of the requested file to the client
         for i in range(0, len(outputdata)):
             connectionSocket.send(outputdata[i].encode())
         connectionSocket.send("\r\n".encode())
         connectionSocket.close()
     except IOError:
         # 回傳網頁未找到
         connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())
         connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
         connectionSocket.send('<html><body><h1>Error</h1><h2>404 Not Found</h2></body></html>'.encode())
		  # close client socket
         connectionSocket.close()     
          
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data