#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:36:04 2021

@author: Xiangyu Ren
"""

import numpy as np
from scapy.all import *
import matplotlib.pyplot as plt

# pkts1 = rdpcap("mab_random_loss1.cap")
# pkts2 = rdpcap("no_mab_random_loss1.cap")
pkts1 = rdpcap("no_mab_fixed_loss.cap")
pkts2 = rdpcap("mab_fixed_loss.cap")


def drawACKCurve(time1, ack1, label1, time2, ack2, label2):
    plt.plot(time1, ack1, label = label1)
    plt.plot(time2, ack2, label = label2)
    plt.xlabel('Reception timestamp (s)')
    plt.ylabel('ACK sequence number')
    plt.title('Packet reception time comparison')
    plt.legend()
    plt.show()
    
    

def drawBoxplot(delay, label):
    plt.boxplot(delay, labels = label)
    plt.ylabel('Delay (s)')
    # plt.xlabel(label)
    plt.title('Per-packet delay Comparison')
    plt.show()

def drawCDF(delay1, delay2, label1, label2, pdf=False):
    count1, bins_count1 = np.histogram(delay1, bins=50)
    count2, bins_count2 = np.histogram(delay2, bins=50)
    pdf1 = count1 / sum(count1)
    cdf1 = np.cumsum(pdf1)
    pdf2 = count2 / sum(count2)
    cdf2 = np.cumsum(pdf2)
    plt.figure()
    plt.plot(bins_count1[0:-1], cdf1, label="withMab")
    plt.plot(bins_count2[0:-1], cdf2, label="noMab")
    plt.legend()
    if pdf == True:
        plt.figure(2)
        plt.plot(bins_count1[0:-1], pdf1, label="withMab")
        plt.plot(bins_count2[0:-1], pdf2, label="noMab")
        plt.legend()
    
    plt.show()


    
    

def collectData(trace):
    clientTime = []
    serverTime = []
    test1 = []
    test2 = []
    data = 0
    flag = -1
        
    for p in trace:
        temp = float(p.time)
        d = str(p[UDP].payload)
        data = int(d[2:-1])
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
    newClientTime = []
    newServerTime = []
    newAckID = []
    j = 0
    k = 0
    # for item in test1:
    #     if item == test2[j]:
    #         newTime.append(clientTime[k])
    #         j += 1
    #     k += 1
    for item in test1:
    # print(k, '---', item)
        if item == test2[j]:
        # print (test2[j])
            newClientTime.append(clientTime[k])
            newServerTime.append(serverTime[j])
            # newAckID.append(item)
            tt = j
            j += 1
            if j == len(test2):
                break
            while test2[j] == test2[tt]:
                j += 1
        k += 1

    ackTime = np.array(newServerTime)
    sendTime = np.array(newClientTime)
    # sendTime = np.array(clientTime)
    # ackTime = np.array(serverTime)
    ackTime = ackTime - sendTime[0]
    sendTime = sendTime - sendTime[0]
    pktDelay = ackTime - sendTime
    sendID = test1
    ackID =  test2
    
    return ackTime, sendTime, pktDelay, sendID, ackID

# Original data
[ackTime1, sendTime1, pktDelay1, sendID1, ackID1] = collectData(pkts1)
[ackTime2, sendTime2, pktDelay2,  sendID2, ackID2]  = collectData(pkts2)
Delay = [pktDelay1, pktDelay2]
# print(sendTime1[0:10],'\n************\n')
# print(ackTime1[0:10],'\n************\n')


# # Filter out outstanding data
# fil_delay1 = pktDelay1[pktDelay1<0.15]
# fil_delay2 = pktDelay2[pktDelay2<0.15]
# fil_Delay = [fil_delay1, fil_delay2]

# ** Boxplot **
# plt.figure(1)
# drawBoxplot(Delay, ['with MAB', 'without MAB'])
# plt.figure(2)
# drawBoxplot(fil_Delay, ['with MAB', 'without MAB'])

# # ** ACK-time curve **
# # t = np.minimum(len(ackTime1), len(ackTime2))
# t = np.linspace(0, 2016, num=1804).astype(int)
# ack1 = sendID1
# ack2 = ackID2
# time1 = sendTime1
# time2 = sendTime2[t]
# plt.figure(3)
# drawACKCurve(time1, ack1, 'with MAB', time2, ack2, 'without MAB')

# ** CDF curve **
drawCDF(pktDelay1, pktDelay2, 'withMAB', 'noMAB', pdf=True)

# count1, bins_count1 = np.histogram(pktDelay1, bins=50)
# count2, bins_count2 = np.histogram(pktDelay2, bins=50)
# pdf1 = count1 / sum(count1)
# cdf1 = np.cumsum(pdf1)
# pdf2 = count2 / sum(count2)
# cdf2 = np.cumsum(pdf2)
# plt.figure(1)
# plt.plot(bins_count1[0:-1], cdf1, label="withMab")
# plt.plot(bins_count2[0:-1], cdf2, label="noMab")
# plt.legend()

# plt.figure(2)
# plt.plot(bins_count1[0:-1], pdf1, label="withMab")
# plt.plot(bins_count2[0:-1], pdf2, label="noMab")
# plt.legend()
# plt.show()



