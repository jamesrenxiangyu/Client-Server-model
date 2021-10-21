# MAB_error_ctl


## MAB Usage
1. python3 receiver.py
2. python3 sender.py IP_address Port_number Required_loss Packet_no

Ip_address: the ip address of where receiver runs
Port_number: the port number is 8888 hardcoded in receiver.py
required_loss: required loss rate
packet_no: how many packets to be sent

## Mininet Usage
For simple version (static loss rate)
1. cd ~/MAB
2. sudo mn --custom finalTopol.py --topo=mytopo -x

For dynamic loss version
1. cd ~/MAB
2. sudo mn --custom Mytopo.py --topo=mytopo
