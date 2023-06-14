#!/usr/bin/python3


import socket
import select


def parse_http(mes):
    s = mes.splitlines()
    c, i = 0, 0

    if len(s) == 0:
        return

    for i in range(len(s)):
        if s[i] == '':
            c += 1
        if c == 1:
            break

    header = s[i:len(s)]
    body = s[i + 1:len(s)]

    return {'code': s[0], 'header': header, 'body': "\n".join(body)}


def calculate(operand: str = '+') -> float:
    if operand in OPERANDS and len(ARGUMENTS) == 2:
        return eval(str(ARGUMENTS[0]) + operand + str(ARGUMENTS[1]))


def get_value(mes):
    if mes['body']:
        return mes['body']


def get_index(mes):
    code = mes['code'].split()
    for arg in code:
        if arg.count(ADD_COMMAND):
            return int(arg[3:len(arg)]) - 1


def build_http(body, code):
    return f'HTTP/1.1 {code}\r\n' + f'Content-Length: {len(body)}\r\n' + '\r\n' + body + '\r\n\r\n'


def send_ans(result, code, sk):
    mes = build_http(result, code).encode()
    print(mes)
    sk.send(mes)


def send_404(sk):
    send_ans('', '404 Not found', sk)


def send_405(sk):
    send_ans('', '405 Not allowed', sk)


def analyze(mes, sk):

    print(mes)

    if mes['code'].count(ADD_COMMAND):

        if mes['code'].count('PUT'):
            index = get_index(mes)
            ARGUMENTS[index] = int(get_value(mes))
            send_ans('', '200 Ok', sk)

        elif mes['code'].count('GET'):
            index = get_index(mes)
            if index in ARGUMENTS:
                send_ans(str(ARGUMENTS[index]), '200 Ok', sk)
            else:
                send_404(sk)

        else:
            send_405(sk)

    elif mes['code'].count(CALC_COMMAND) and mes['code'].count('POST'):
        operand = get_value(mes)
        result = 0

        if operand:
            result = calculate(operand)
            print(result)
        else:
            result = calculate()

        if result:
            send_ans(str(result), '200 Ok', sk)
        else:
            send_405(sk)

    else:
        send_404(sk)


def handler(sk, addr):
    ans = b' '

    while len(ans) != 0:
        ans = sk.recv(BUF_SIZE)
        mes = parse_http(ans.decode())
        if mes:
            analyze(mes, sk)


def work(server):
    while True:
        sk, addr = server.accept()
        handler(sk, addr)


BUF_SIZE = 1_000_000
ADDR = ('localhost', 10_000)
COUNT_OF_CLIENTS = 10
ADD_COMMAND = '/op'
CALC_COMMAND = '/calculate'
OPERANDS = ['+', '-', '*', '/']
ARGUMENTS = dict()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)
server.listen(COUNT_OF_CLIENTS)

work(server)
