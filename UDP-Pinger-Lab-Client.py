# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 22:30:12 2018

@author: craig
"""

from socket import *
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)

# To set waiting time of one second for reponse from server
clientSocket.settimeout(1)

# Declare server's socket address
server_ip = "192.168.1.101"
remoteAddr = (server_ip, 12000)

# Ping ten times
for i in range(10): #跑十次
    sendTime = time.time()
    message = 'PING ' + str(i + 1) + "_" + str(time.strftime("%H:%M:%S"))
    clientSocket.sendto(message.encode(), remoteAddr)
    
    try:
        data, server = clientSocket.recvfrom(1024)
        recdTime = time.time()
        RTT = recdTime - sendTime
        print("Message Received", data)
        print ("Round Trip Time", RTT)

    except timeout:
        print(".REQUEST TIMED OUT")