#!/usr/bin/python3


import scapy.all as sc
import sys
import random as rd


def get_seq_ack(pkt):
    return pkt[sc.TCP].seq, pkt[sc.TCP].ack


def count_seq_akc(pkt):
    if not sc.TCP in pkt:
        print(pkt)
        return None
    p, seq, ack = pkt[sc.TCP], 0, 0
    print(f':::{p.payload.load}')
    if 'S' in p.flags or 'F' in p.flags:
        ack, seq = p.seq + 1, p.ack
    elif p.payload.load != None:
        ack, seq = p.seq + len(p.payload.load), p.ack
    else:
        ack, seq = p.seq + 1, p.ack
    return seq, ack


def get_ack(req, seq, ack):
    seq, ack = count_seq_akc(req)
    p = get_tcp(seq, ack, 'A')
    return p


def get_tcp(seq, ack, flags, payload=None):
    tcp = sc.TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags=flags)
    raw = sc.Raw(load=payload)
    return eth / ip / tcp / raw


def ftp_cmd(cmd, arg_str):
    pkt = get_tcp(seq, ack, 'S', cmd + " " + arg_str)
    print(pkt.show())
    ans = sc.srp(pkt)[0][0][1][sc.Raw].load.split(' ')
    return (ans[0], ans[1:len(ans)])


def send_SYST(seq, ack):
    return get_tcp(seq, ack, '', 'SYST\r\n')


def get_mes(pkt):
    return bytes(pkt)


def main():
    ack, seq = 0, 0

    ans = sc.srp(get_tcp(20, 0, 'S'))
    p = ans[0][0][1]

    p = get_ack(p, seq, ack)
    seq, ack = get_seq_ack(p)
    ans = sc.sendp(p)

    ans = sc.srp(send_SYST(seq, ack))[0][0][1]
    seq, ack = get_seq_ack(ans)

    ans = get_ack(ans, seq, ack)
    seq, ack = get_seq_ack(ans)
    ans = sc.sendp(ans)

    ans = sc.srp(get_tcp(seq + 1, ack - 1, 'F'))
    p = ans[0][0][1]

    p = get_ack(p, seq, ack)
    seq, ack = count_seq_akc(p)
    ans = sc.sendp(p)


if __name__ == "__main__":
    ack, seq = 0, 0
    sport = 24972
    dport = 21
    eth = sc.Ether(dst="52:54:00:12:35:02", src="08:00:27:e5:5c:5f")
    ip = sc.IP(src="10.0.2.15", dst="194.108.117.16")
    main()





