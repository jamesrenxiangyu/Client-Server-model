import os
import time
from mininet.net import Mininet
# from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.node import Node, Host, Switch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI

import sys

def linkUpdate(net, n1, n2, link, totalTime, currentTime, currentLoss, lossStep, serverIp, port, targetLoss, numPacket):
    i = 0
    info("*** Update Link Param\n")
    CLI(net, script = 'clientScript.txt')
    CLI(net, script = 'serverScript.txt')
    while True:
        # n2.cmd('python3 sender.py %s %s %s %s', (serverIp, port, targetLoss, numPacket))
        if currentTime > totalTime:
            break;
        if time.time() - currentTime > i+10:
            info("\n*** Link Update")
            link.delete()
            currentLoss += lossStep
            link.__init__(n1, n2, cls = TCLink, bw = 100, delay = 10, loss = currentLoss)
            i += 10

def topology():
    info("Create a network.")
    net = Mininet(link=TCLink)
    global gnet
    gnet = net

    clientIp = '10.0.0.1/8'
    serverIp = '10.0.0.2/8'
    port = 8888
    targetLoss = 5
    numPacket = 10

    info("*** Setting parameter\n")
    totalTime = time.time() + 100  # total time = 100 seconds
    currentTime = time.time()
    currentLoss = 0
    lossStep = 2


    info("*** Creating nodes\n")
    leftHost = net.addHost('c1', cls = Host, ip = clientIp)
    rightHost = net.addHost('s1', cls = Host, ip = serverIp)
    switch = net.addSwitch('sw1', cls = Switch)

    info("*** Creating link\n")
    l1 = net.addLink(leftHost, switch, cls=TCLink, delay = 3, loss = 5)
    l2 = net.addLink(rightHost, switch, cls=TCLink, delay = 3, loss = 5)

    info("*** Starting network\n")
    net.build()

    info("*** Enable Client-Socket model\n")  
    # rightHost.cmd('python3 receiver.py')
    # print("*** Receiver started ...")

    # linkUpdate(net, leftHost, rightHost, l1, totalTime, currentTime, currentLoss, lossStep, serverIp, port, targetLoss, numPacket)	
   
    # kills all the xterms that have been opened
    # os.system('pkill xterm')

    info ("*** Running CLI\n")
    CLI(net)

    info ("*** Stopping network\n")
    net.stop()

topos = { 'mytopo': ( lambda: topology() ) }    

if __name__ == '__main__':
    setLogLevel('info')
    try:
        topology()
    except:
        type = sys.exc_info()[0]
        error = sys.exc_info()[1]
        traceback = sys.exc_info()[2]
        print ("Type: %s" % type)
        print ("Error: %s" % error)
        print ("Traceback: %s" % traceback)
        if gnet != None:
            gnet.stop()
        else:
            print("No network was created...")