# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 17:51:49 2018

@author: craig
"""

import socket
import sys
 
target_host = "192.168.1.101"
target_port = 1515
 
# create socket
# AF_INET 代表使用標準 IPv4 位址或主機名稱
# SOCK_STREAM 代表這會是一個 TCP client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# client 建立連線
client.connect((target_host, target_port))
 
# 傳送資料給 target
client.send(('GET /'+str(sys.argv[3])+' HTTP/1.1\r\n\r\n').encode())

response = client.recv(4096)

print(response)