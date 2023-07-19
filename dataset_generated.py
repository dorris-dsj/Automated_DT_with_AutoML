import random
import csv
import numpy as np
import time
import os

from mininet.net import Mininet
from mininet.node import CPULimitedHost,OVSSwitch
from mininet.link import TCLink

'''
file_path='datatest.txt'

with open(file_path,'w',newline='') as file:
    writer=csv.writer(file,delimiter='\t')
    
    for _ in range(12):
        data=[random.randint(1,100) for _ in range(6)]
        writer.writerow(data)
        
        #if file.tell() % (6*(len(str(data[0]))+1)) == 0:
        #    writer.writerow([])
            
print('saved')
'''



def create_topology(queue_size,file_path,i):
    net = Mininet(host=CPULimitedHost, switch=OVSSwitch, link=TCLink)
    #, ip='10.0.1.1/24'
    client=net.addHost('client', ip='20.0.1.1/24')
    server=net.addHost('server', ip='30.0.1.1/24')
    r1=net.addHost('r1',ip='20.0.1.2/24')
    r2=net.addHost('r2',ip='40.0.1.2/24')
    r3=net.addHost('r3',ip='50.0.1.2/24')
    r4=net.addHost('r4',ip='60.0.1.2/24')
    #net.get('r1').setIP('10.0.0.3/24')
    
    array=np.empty(6)
    
    array[0]=queue_size[0]
    array[1]=queue_size[1]
    array[2]=queue_size[2]
    array[3]=queue_size[3]
    
    link1=net.addLink(client,r1,delay='20ms',bw=200,loss=0,use_htb=True)
    link2=net.addLink(r1,r2,delay='20ms',max_queue_size=array[0]*1024,bw=400,loss=0,use_htb=True)
    link3=net.addLink(r2,r4,delay='20ms',max_queue_size=array[1]*1024,bw=400,loss=0,use_htb=True)
    link4=net.addLink(r1,r3,delay='40ms',max_queue_size=array[0]*1024,bw=400,loss=0,use_htb=True)  
    link5=net.addLink(r3,r4,delay='40ms',max_queue_size=array[2]*1024,bw=400,loss=0,use_htb=True)
    link6=net.addLink(server,r4,delay='20ms',max_queue_size=array[3]*1024,bw=400,loss=0,use_htb=True) 
      
    
    #r1.intf('r1-eth0').setIP('20.0.1.2/24')
    
    r1.intf('r1-eth1').setIP('40.0.1.1/24')
    r1.intf('r1-eth2').setIP('50.0.1.1/24')
    r2.intf('r2-eth1').setIP('60.0.1.1/24')
    r3.intf('r3-eth1').setIP('70.0.1.1/24')
    r4.intf('r4-eth1').setIP('70.0.1.2/24')
    r4.intf('r4-eth2').setIP('30.0.1.2/24')
    
    
    
    start_time = time.time ()
    
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
    
    
    server.cmd('python -m http.server 80 &')    
    
    start_time_download=time.time()
    client.cmd('wget -O download_file http://30.0.1.1:80/file.txt')
    end_time_download=time.time()
    array[4]=end_time_download-start_time_download
    
    os.remove('download_file')
    
    
    #print("Average Delay of path 1:",avg_delay_1)
    
    r1.cmd('route del -net 30.0.1.0/24 gw 40.0.1.2 dev r1-eth1')
    
    r4.cmd('route del -net 20.0.1.0/24 gw 60.0.1.1 dev r4-eth0')
    
    
    r1.cmd('route add -net 30.0.1.0/24 gw 50.0.1.2 dev r1-eth2')
    r4.cmd('route add -net 20.0.1.0/24 gw 70.0.1.1 dev r4-eth1')
    
    start_time_download=time.time()
    client.cmd('wget -O download_file http://30.0.1.1:80/file.txt')
    end_time_download=time.time()
    array[5]=end_time_download-start_time_download
    
    os.remove('download_file')
    
    #print("Average Delay of path 2:",avg_delay_2)
    
    
    #file_path='datatest.txt'
    
    #
    with open(file_path,'a',newline='') as file:
        writer=csv.writer(file)
        #,delimiter=','
        writer.writerow(array)
    
    print('saved ',i+1)
    
    
    #net.interact()
    net.stop()
    
    end_time=time.time()
    
    total_duration=end_time-start_time
    
    with open('time.csv','a',newline='') as file:
        file.write(str(total_duration)+'\n')


def check_duplicates(arrays,new_array):
    array_set=set(tuple(array) for array in arrays)
    return tuple(new_array) in array_set
    
    
if __name__=="__main__":
    file_path='datatest.csv'
    with open(file_path,'w') as file:
        file.truncate(0)
    
    with open('time.csv','w') as file:
        file.truncate(0)
    
    queue_size_arrays=[]
    
    for i in range(5000):
        new_queue_size=[random.randint(80,120) for _ in range(4)]
        
        while check_duplicates(queue_size_arrays,new_queue_size):
            new_queue_size = [random.randint(80,120) for _ in range(4)]
        queue_size_arrays.append(new_queue_size)
        
        create_topology(new_queue_size,file_path,i) 
        new_queue_size=[]
        
    
    for i in range(5000):
        new_queue_size=[random.randint(50,150) for _ in range(4)]
        
        while check_duplicates(queue_size_arrays,new_queue_size):
            new_queue_size = [random.randint(80,120) for _ in range(4)]
        queue_size_arrays.append(new_queue_size)
        
        create_topology(new_queue_size,file_path,i) 
        new_queue_size=[]
    
    
    for i in range(5000):
        new_queue_size=[random.randint(50,200) for _ in range(4)]
        
        while check_duplicates(queue_size_arrays,new_queue_size):
            new_queue_size = [random.randint(50,200) for _ in range(4)]
        queue_size_arrays.append(new_queue_size)
        
        create_topology(new_queue_size,file_path,i) 
        new_queue_size=[]
        
        
    for i in range(5000):
        new_queue_size=[random.randint(10,200) for _ in range(4)]
        
        while check_duplicates(queue_size_arrays,new_queue_size):
            new_queue_size = [random.randint(10,200) for _ in range(4)]
        queue_size_arrays.append(new_queue_size)
        
        create_topology(new_queue_size,file_path,i) 
        new_queue_size=[]
    

