#!/usr/bin/python3


import socket
from ast import literal_eval as make_tuple
import sys


def quit(sk, shut):
    ans = ' '
    data = b''
    sk.shutdown(shut)
    while len(ans) != 0:
        ans = sk.recv(buf_size)
        data += ans
    return data


def get_ans(buf_size):
    ans = sk.recv(buf_size)
    return ans.decode()


def parse_addr(ans):
    addr = make_tuple(ans.split()[-1])
    ip = tuple(map(str, addr))[0:4]
    return (".".join(ip), addr[-2] << 8 | addr[-1])


def download_data(addr):
    d_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    d_sk.connect(d_addr)

    file = d_sk.recv(buf_size)

    file += quit(d_sk, socket.SHUT_WR)
    d_sk.close()

    return file


def log_in(login, password):
    print(f'--> USER {login}')
    sk.send(f'USER {login}\r\n'.encode())

    ans = get_ans(buf_size)
    print(f'<-- {ans}')

    if ans.count('331'):
        print(f'--> PASS {password}')
        sk.send(f'PASS {password}\r\n'.encode())
        
        ans = get_ans(buf_size)
        print(f'<-- {ans}')
        
        return ans.count('230')
    return 0


def to_pasv_mode():
    print('--> PASV')
    sk.send(b'PASV\r\n')

    ans = get_ans(buf_size)
    print(f'<-- {ans}')
    
    return ans


def retr(path):
    print(f'--> RETR to {path}')
    sk.send(f'RETR {path}\r\n'.encode())

    ans = get_ans(buf_size)
    print(f'<-- {ans}')  
    
    return ans.count('150')

host_name, login, password, path = sys.argv[1:len(sys.argv)]
host = socket.gethostbyname(host_name)

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = (host, 21)
buf_size = 1_000_000
ans = b' '
file = ''

sk.connect(addr)

print(f'<-- {get_ans(buf_size)}')

if log_in(login, password):
    ans = to_pasv_mode()
    if ans.count('227'):
        d_addr = parse_addr(ans)
        print(f'Download address: {d_addr}')
         
        if retr(path):
            file = download_data(d_addr)

            print('<-- File:')
            with open('out.png', 'wb') as out:
                out.write(file)

quit(sk, socket.SHUT_WR)
sk.close()
