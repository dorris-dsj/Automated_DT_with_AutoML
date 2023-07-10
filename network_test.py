import time
import os
from mininet.net import Mininet
from mininet.node import CPULimitedHost,OVSSwitch
from mininet.link import TCLink

def create_topology():
    net = Mininet(host=CPULimitedHost, switch=OVSSwitch, link=TCLink)
    #, ip='10.0.1.1/24'
    client=net.addHost('client', ip='20.0.1.1/24')
    server=net.addHost('server', ip='30.0.1.1/24')
    r1=net.addHost('r1',ip='20.0.1.2/24')
    r2=net.addHost('r2',ip='40.0.1.2/24')
    r3=net.addHost('r3',ip='50.0.1.2/24')
    r4=net.addHost('r4',ip='60.0.1.2/24')
    #net.get('r1').setIP('10.0.0.3/24')
    
    link1=net.addLink(client,r1,delay='20ms')
    link2=net.addLink(r1,r2,delay='20ms')
    link3=net.addLink(r2,r4,delay='20ms')
    link4=net.addLink(r1,r3,delay='40ms')  
    link5=net.addLink(r3,r4,delay='40ms')
    link6=net.addLink(server,r4,delay='20ms') 
      
    
    #r1.intf('r1-eth0').setIP('20.0.1.2/24')
    
    r1.intf('r1-eth1').setIP('40.0.1.1/24')
    r1.intf('r1-eth2').setIP('50.0.1.1/24')
    r2.intf('r2-eth1').setIP('60.0.1.1/24')
    r3.intf('r3-eth1').setIP('70.0.1.1/24')
    r4.intf('r4-eth1').setIP('70.0.1.2/24')
    r4.intf('r4-eth2').setIP('30.0.1.2/24')
    
    queue1=200
    queue2=200
    queue3=200
    queue4=200
    link1.intf1.config(**{'max_queue_size':queue1})
    link2.intf1.config(**{'max_queue_size':queue2})
    link3.intf1.config(**{'max_queue_size':queue4})
    link4.intf1.config(**{'max_queue_size':queue3})
    link5.intf1.config(**{'max_queue_size':queue4})
    link6.intf1.config(**{'max_queue_size':queue4})
    
    
    
    net.build()
    net.start()
    
    r1.cmd('sysctl net.ipv4.ip_forward=1')
    r2.cmd('sysctl net.ipv4.ip_forward=1')
    r3.cmd('sysctl net.ipv4.ip_forward=1')
    r4.cmd('sysctl net.ipv4.ip_forward=1')   
    client.cmd('route add default gw 20.0.1.2 dev client-eth0')
    server.cmd('route add default gw 30.0.1.2 dev server-eth0')
    
    
    r2.cmd('route add -net 30.0.1.0/24 gw 60.0.1.2 dev r2-eth1')
    r2.cmd('route add -net 20.0.1.0/24 gw 40.0.1.1 dev r2-eth0')
    
    r3.cmd('route add -net 30.0.1.0/24 gw 70.0.1.2 dev r3-eth1')
    r3.cmd('route add -net 20.0.1.0/24 gw 50.0.1.1 dev r3-eth0')
    
    r4.cmd('route add -net 30.0.1.0/24 gw 30.0.1.1 dev r4-eth2')
    r1.cmd('route add -net 20.0.1.0/24 gw 20.0.1.1 dev r1-eth0')
    
    
    r1.cmd('route add -net 30.0.1.0/24 gw 40.0.1.2 dev r1-eth1')

    r4.cmd('route add -net 20.0.1.0/24 gw 60.0.1.1 dev r4-eth0')
    
    #net.cmd('link link1 delay 100ms')
    
    server.cmd('python -m http.server 80 &')
    
    start_time=time.time()
    client.cmd('wget -O download_file http://30.0.1.1:80/file.txt')
    end_time=time.time()
    download_time=end_time-start_time
    print("Average Delay of path 1:",download_time)
    
    os.remove('download_file')
    
    r1.cmd('route del -net 30.0.1.0/24 gw 40.0.1.2 dev r1-eth1')
    
    r4.cmd('route del -net 20.0.1.0/24 gw 60.0.1.1 dev r4-eth0')
    
    
    r1.cmd('route add -net 30.0.1.0/24 gw 50.0.1.2 dev r1-eth2')
    r4.cmd('route add -net 20.0.1.0/24 gw 70.0.1.1 dev r4-eth1')
    
    
    start_time=time.time()
    client.cmd('wget -O download_file http://30.0.1.1:80/file.txt')
    end_time=time.time()
    download_time=end_time-start_time
    print("Average Delay of path 2:",download_time)
    
    os.remove('download_file')
    
    net.interact()
    net.stop()
    
    
if __name__=="__main__":
    create_topology() 
    
    
    
    
    
    '''
    ping_output=client.cmd('ping -c 12 -s 100 30.0.1.1')
    
    rtt_values=[]
    for line in ping_output.split('\n'):
        if 'rtt' in line:
            rtt=line.split('/')[4]
            rtt_values.append(float(rtt))
            
    avg_delay=sum(rtt_values[-10:])/10
    '''
