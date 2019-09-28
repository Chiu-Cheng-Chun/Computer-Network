# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 18:10:26 2018

@author: craig
"""

from socket import *
import time
import numpy as np

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)

# To set waiting time of one second for reponse from server
clientSocket.settimeout(1)

# Declare server's socket address
server_ip = "192.168.1.101"
remoteAddr = (server_ip, 12000)

RTT = []
timeouts = 0

# Ping ten times
for i in range(10): #跑十次
    sendTime = time.time()
    message = 'PING ' + str(i + 1) + "_" + str(time.strftime("%H:%M:%S"))
    clientSocket.sendto(message.encode(), remoteAddr)
    
    try:
        data, server = clientSocket.recvfrom(1024)
        recdTime = time.time()
        RTT = np.append(RTT, recdTime - sendTime)
        print("Message Received", data)
        print ("Round Trip Time", recdTime - sendTime)

    except timeout:
        timeouts += 1
        print(".REQUEST TIMED OUT")

print("Minimun RTT:", min(RTT),"\nMaximun RTT:",max(RTT),"\nAverage RTT:",np.mean(RTT),"\nLoss Rate:",timeouts*100/10,"%")