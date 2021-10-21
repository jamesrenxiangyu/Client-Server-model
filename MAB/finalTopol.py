"""Custom topology example

Two directly connected switches plus a host for each switch:

   client --- switch --- server

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""
import os
import time
from mininet.net import Mininet
# from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.node import Node, Host, Switch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import sys
from mininet.topo import Topo

# def changeLoss():
#   for intf in node.intfList(): # loop on interfaces of node
#     #info( ' %s:'%intf )
#     if intf.link: # get link that connects to interface(if any)
#         newBW = 5
#         intfs = [ intf.link.intf1, intf.link.intf2 ] #intfs[0] is source of link and intfs[1] is dst of link
#         intfs[0].config(bw=newBW) 
#         intfs[1].config(bw=newBW)
#     else:
#         info( ' \n' )

# def linkUpdate(link, totalTime, currentTime, n1, n2, currentLoss, lossStep):
#     i = 0
#     info("*** Update Link Param\n")
#     while True:
#         if currentTime > totalTime:
#             break;
#         if time.time() - currentTime > i+5:
#             link.delLink()
#             link.addLink(n1, n2, cls = TCLink, bw = 100, delay = 10, loss = currentLoss+i*lossStep)
#             i += 5


class MyTopo( Topo ):
    print("Simple topology example.")

    def __init__( self ):
        print("Create custom topo.")
        totalTime = time.time() + 100  # total time = 100 seconds
        currentTime = time.time()
        currentLoss = 5
        lossStep = 2

        # Initialize topology
        Topo.__init__( self)

        # Add hosts and switches
        info( "*** Creating nodes\n" )
        leftHost = self.addHost( 'c1' , ip = '10.0.0.1/8')
        rightHost = self.addHost( 's1', ip = '10.0.0.2/8' )
        leftSwitch = self.addSwitch( 'sw1' )

        info( "*** Creating links\n" )  
        l1 = self.addLink( leftHost, leftSwitch, cls = TCLink, bw = 100, delay = 10, loss = currentLoss)
        l2 = self.addLink( rightHost,leftSwitch, cls = TCLink, bw = 100, delay = 10, loss = currentLoss)

        # rightHost.cmd('python3 receiver.py')
        # leftHost.cmd('python3 sender.py 10.0.0.2 8888 5 100')

        # linkUpdate(l1, totalTime, currentTime, leftHost, leftSwitch, currentLoss, lossStep)	
        


topos = { 'mytopo': ( lambda: MyTopo() ) }

