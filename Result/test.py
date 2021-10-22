#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:36:04 2021

@author: cailab
"""

import numpy as np
from scapy.all import *
import matplotlib.pyplot as plt

pkts1 = rdpcap("mab_random_loss.cap")


clientTime = []
serverTime = []
test1 = []
test2 = []
data = 0
flag = '-1'
    
for p in pkts1:
    temp = float(p.time)
    data = str(p[UDP].payload)
    # print('** send: ', data)
    if p[IP].src == '192.168.1.100' and data != flag:
        clientTime.append(temp)
        test1.append(data)
        # print('sendID', data)
    elif p[IP].src == '10.10.1.100' and data == flag:
        serverTime.append(temp)
        test2.append(data)
        # print('ackID', data)
    flag = data
    
flag2 = 0
newTime = []
j = 0
k = 0
for item in test1:
    if item == test2[j]:
        newTime.append(clientTime[k])
        j += 1
    k += 1
ackTime = np.array(serverTime)
sendTime = np.array(newTime)
pktDelay = ackTime - sendTime