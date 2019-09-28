# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 18:23:42 2018

@author: craig
"""

# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
host = '' #預設localhost
Port = 12000 #port_number
serverSocket.bind((host, Port))

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    # Capitalize the message from the client
    message = message.upper()
    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 3:
        continue
    # Otherwise, the server responds
    else:
        serverSocket.sendto(message, address)