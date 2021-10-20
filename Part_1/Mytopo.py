from mininet.net import Mininet
from mininet.node import Node
from mininet.node import Host
from mininet.node import Switch
from mininet.link import TCLink
from mininet.log import  setLogLevel, info
from threading import Timer
from mininet.util import quietRun
from time import sleep



def myNet(cargs='-v ptcp:'):
    net = Mininet(topo = False)

    "Create network from scratch using Open vSwitch."
    info( "*** Creating nodes\n" )
    s0 = net.addSwitch('s0', cls=Switch)
    h0 = net.addHost('h0', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)    
    # s0 = Node( 's0', inNamespace=False )
    # # switch1 = Node( 's1', inNamespace=False )
    # h0 = Node( 'h0' )
    # h1 = Node( 'h1' )
    
    info( "*** Creating links\n" )
    linkopts0=dict(bw=100, delay='1ms', loss=0)
    linkopts1=dict(bw=100, delay='1ms', loss=10)
    link0 = TCLink( h0, s0, **linkopts0)
    link1 = TCLink( s0, h1, **linkopts1)     
    # link2 = TCLink( h1, switch1, **linkopts0)
    #print link0.intf1, link0.intf2
    link0.intf2.setMAC("0:0:0:0:0:1")
    link1.intf1.setMAC("0:0:0:0:0:2")
    link1.intf2.setMAC("0:1:0:0:0:1") 
    # link2.intf2.setMAC("0:1:0:0:0:2")
 
    info( "*** Configuring hosts\n" )
    h0.setIP( '192.168.123.1/24' )
    h1.setIP( '192.168.123.2/24' )
       
    info( "*** Starting network using Open vSwitch\n" )
    s0.cmd( 'ovs-vsctl del-br dp0' )
    s0.cmd( 'ovs-vsctl add-br dp0' )

    info( '*** Starting network\n')
    net.build()



topos = { 'mytopo': ( lambda: myNet() ) }    