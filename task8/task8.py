#!/usr/bin/python3


import socket
import select


def parse_header(header):
    data = dict()
    for item in header:
        item = item.split(': ')
        data[item[0]] = item[1]
    return data


def parse_http(mes):
    header_and_body = mes.split('\r\n\r\n')
    code_and_header = header_and_body[0].split('\r\n')
    
    code = code_and_header[0]
    header = parse_header(code_and_header[1:len(code_and_header)])
    body = None
    if len(header_and_body) > 1:
        body = header_and_body[1]

    if code:
        return {'code': code, 'header': header, 'body': body}


def calculate(operand: str = '+') -> float:
    print(ARGUMENTS)
    if operand in OPERANDS and len(ARGUMENTS) == 2:
        return eval(str(ARGUMENTS[0]) + operand + str(ARGUMENTS[1]))


def get_value(mes):
    if mes['body']:
        try:
            return int(mes['body'])
        except ValueError:
            pass


def get_body(mes):
    if mes['body']:
        return mes['body']


def get_index(mes):
    code = mes['code'].split()
    for arg in code:
        if arg.count(ADD_COMMAND):
            try:
                return int(arg[3:len(arg)]) - 1
            except ValueError:
                pass


def build_http(body, code):
    return f'HTTP/1.1 {code}\r\n' + f'Content-Length: {len(body)}\r\n\r\n' + body + '\r\n'


def send_ans(result, code, sk):
    mes = build_http(result, code).encode()
    print(mes)
    sk.send(mes)


def send_404(sk):
    send_ans('', '404 Not found', sk)


def send_405(sk):
    send_ans('', '405 Not allowed', sk)


def send_value_ans(index, sk):
    if index in ARGUMENTS:
        send_ans(str(ARGUMENTS[index]), '200 Ok', sk)
    else:
        send_404(sk)


def analyze_ADD_COMMAND(mes, sk):
    if mes['code'].count('PUT'):
        index = get_index(mes)
        value = get_value(mes)

        if index != None and value != None:
            ARGUMENTS[index] = value
            send_ans('', '200 Ok', sk)
            return True
            
    elif mes['code'].count('GET'):
        index = get_index(mes)
        
        if index != None:
            send_value_ans(index, sk)
            return True


def analyze_CALC(mes, sk):
    operand = None
    result = 0
    
    if 'header' in mes:
        if 'Operation' in mes['header']:
            operand = mes['header']['Operation']

    if operand:
        result = calculate(operand)
    else:
        result = calculate()

    if result != None:
        send_ans(str(result), '200 Ok', sk)
        return True


def analyze(mes, sk):

    print(mes)

    if mes['code'].count(ADD_COMMAND):
        if not analyze_ADD_COMMAND(mes, sk):
            send_405(sk)

    elif mes['code'].count(CALC_COMMAND) and mes['code'].count('POST'):
        if not analyze_CALC(mes, sk):
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
