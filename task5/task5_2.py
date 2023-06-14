#!/usr/bin/python3


import scapy.all as sp
import time
import signal
import json


def init_seq(data, pkt):

    icmp = pkt[sp.ICMP]
    ip = pkt[sp.IP]
    
    if icmp.id in data.keys():
        
        pkt_type = "Req" if icmp.type == 0 else "Rep"
        
        data[icmp.id] += [{"id": icmp.id, 
                            "seq": icmp.seq,
                            "src": ip.src,
                            "dst": ip.dst,
                            pkt_type: pkt.time}]

    else:
        data[icmp.id] = []
        init_seq(data, pkt)


def req_or_rep(nresponses, nrequests, pkt):
    if 'Rep' in pkt:
        nresponses += 1
    elif 'Req' in pkt:
        nrequests += 1
    
    return nresponses, nrequests


def analyze_data():
    for session in icmps.keys():
    
        s = icmps[session]
        nresponses = 0
        nrequests = 0
        t = []
        
        for i in range(len(s) - 1):
        
            nresponses, nrequests = req_or_rep(nresponses, nrequests, s[i])
                
            for j in range(i + 1, len(s)):
            
                if s[i]['seq'] == s[j]['seq']:
                    t += [s[j]['Req'] - s[i]['Rep']]
        
        nresponses, nrequests = req_or_rep(nresponses, nrequests, s[-1])
        
        result[session] = {'id': session,
                        'src': s[i]['src'],
                        'dst': s[i]['dst'],
                        'nrequests': nrequests,
                        'nresponses': nresponses,
                        'min': min(t),
                        'max': max(t)}    
                        

def show_pkt(pkt):
    if sp.ICMP in pkt and sp.IP in pkt:
        init_seq(icmps, pkt)


icmps = dict()
result = dict()

try:
    pkts = sp.sniff(filter='icmp', prn=show_pkt)
except KeyboardInterrupt:
    pass
    
analyze_data()
print(json.dumps(result, indent=True))
