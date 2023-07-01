#!/usr/bin/python3


import scapy.all as sc
import sys
import random as rd


def get_seq_ack(pkt):
    return pkt[sc.TCP].seq, pkt[sc.TCP].ack


def count_seq_ack(pkt):
    p, seq, ack = pkt[sc.TCP], 0, 0

    if 'S' in p.flags or 'F' in p.flags:
        ack, seq = p.seq + 1, p.ack
    elif p.payload.load:
        ack, seq = p.seq + len(p.payload.load), p.ack
    else:
        ack, seq = p.seq + 1, p.ack
    return seq, ack


def get_ack(req):
    seq, ack = count_seq_ack(req)
    p = get_tcp(seq, ack, 'A')
    return p


def get_tcp(seq, ack, flags, payload=None):
    tcp = sc.TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags=flags)
    raw = sc.Raw(load=payload)
    return eth / ip / tcp / raw


def send_SYST(seq, ack):
    return get_tcp(seq, ack, '', 'SYST\r\n')


def get_mes(pkt):
    return bytes(pkt)


def is_answer_ip(pkt):
    if sc.TCP in pkt:
        return pkt[sc.IP].dst == IP_SRC and pkt[sc.IP].src == IP_DST
    return False


def is_answer_tcp(pkt):
    if sc.TCP in pkt:
        return pkt[sc.TCP].dport == sport and pkt[sc.TCP].sport == dport
    return False


def is_fin_ack(pkt):
    if sc.TCP in pkt and sc.IP in pkt:
        return is_answer_ip(pkt) and is_answer_tcp(pkt) and pkt[sc.TCP].flags == 'FA'
    return False


def send_ack(pkt):
    pkt = get_ack(pkt)
    sc.sendp(pkt)
    return pkt


def connect():
    pkt = sc.srp(get_tcp(20, 0, 'S'))[0][0][1]

    ans = send_ack(pkt)

    if sc.TCP in pkt and pkt[sc.TCP].flags == 'SA':
        return get_seq_ack(ans)


def disconnect(seq, ack):
    sniffer = sc.AsyncSniffer(lfilter=is_fin_ack,
                              iface=IFACE,
                              count=1,
                              timeout=TIMEOUT)      # for waiting FA pkt
    sniffer.start()

    ans = sc.srp(get_tcp(seq, ack, 'FA'))[0][0][1]

    if sc.TCP in ans and ans[sc.TCP].flags == 'A':
        sniffer.join()
        pkt = sniffer.results[0][0][1]
        if pkt:
            send_ack(pkt)

            return count_seq_ack(pkt)


def main():

    res = connect()

    if not res:
        print('Connection error(')
        return None
    seq, ack = res

    print('STATUS: Program connected')

    print('---> SYST')
    pkt = sc.srp(send_SYST(seq, ack))[0][0][1]
    print(f'<--- {pkt.payload.load}')

    ans = send_ack(pkt)
    seq, ack = get_seq_ack(ans)

    print('STATUS: SYST was sent successfuly')

    if not disconnect(seq, ack):
        print('Disconnection error(')
        return None

    return True


# sudo iptables -A OUTPUT -p tcp -m tcp --tcp-flags RST RST -j DROP

if __name__ == "__main__":
    IP_SRC, IP_DST = "10.0.2.15", "194.108.117.16"
    TIMEOUT = 10
    IFACE = 'enp0s3'
    sport = 24972
    dport = 21
    eth = sc.Ether(dst="52:54:00:12:35:02", src="08:00:27:e5:5c:5f")
    ip = sc.IP(src=IP_SRC, dst=IP_DST)
    if main():
        print('Program ended successfully')





