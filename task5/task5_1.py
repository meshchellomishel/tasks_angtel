#!/usr/bin/python3


import scapy.all as sc
import time
import json
import signal
import sys


def check_time_pkts():
    new_data = dict()
    
    for pkt in data:
        age = time.time() - data[pkt]['age']
        if age < 5:
            new_data[pkt] = data[pkt]
            new_data[pkt]['age'] = age
    
    return new_data


def process_IP(pkt):
    if sc.IP in pkt and sc.Ether in pkt:
        ip = pkt[sc.IP]
        eth = pkt[sc.Ether]
        data[ip.dst] = {'mac': eth.dst, 'age': time.time()}
    

def task1():
    sniffer = sc.sniff(prn=process_IP, count=50)
    data = check_time_pkts()
    print(json.dumps(data, indent=True))
    

data = dict()  
task1()


