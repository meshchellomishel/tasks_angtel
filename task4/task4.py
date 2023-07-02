#!/usr/bin/python3


import signal
import time
import sys
import os
import subprocess as sb
import json


def about_cmd(name, stdout=None):
    res = {'name': name}
    if stdout:
        res['out'] = stdout
    return res


def write_terminated(data):
    data[-1]['code'] = -10
    data[-1]['signal'] = 'Terminated'


def end_prog():
    for cmd in data:
        print(json.dumps(cmd, indent=True))


def run_proc(args, subprocesses, In=None, out=sb.PIPE, text=True):
    print(f'running... {args}')
    
    pr = sb.Popen(args, stdin=In, stdout=out, text=text)
    subprocesses += [pr]
    pr.wait()
    subprocesses.pop(-1)

    print(f'finished')
    return pr
    

def handler(sig_num, frame):
    write_terminated(data)
    end_prog()
    subprocesses[-1].terminate()
    sys.exit()


def check_file(args):
    try:
        return args[-2] == "<"
    except IndexError:
        return False
    

def analyze_args(data, argv, index, subprocesses, stdin=sb.PIPE, stdout=sb.PIPE):
    pr = 0
    if index != len(argv):
        args = argv[index].split()
        
        if check_file(args):
            subproc = args[0:len(args)-2]
            
            with open(args[-1], "w+") as file:
                data += [about_cmd(args[0], file.name)]
                pr = run_proc(subproc, subprocesses, In=stdin, out=file)

        else:
            data += [about_cmd(args[0])]
            pr = run_proc(args, subprocesses, In=stdin, out=stdout)
        
        data[-1]['code'] = pr.returncode
        analyze_args(data, argv, index + 1, subprocesses, pr.stdout)


argv = sys.argv
argv = " ".join(argv[1:len(argv)])

signal.signal(signal.SIGUSR1, handler)

data = []
subprocesses = []

try:
    if argv.count('|') != 0:
        argv = argv.split('|')

        analyze_args(data, argv, 0, subprocesses)
    else:
        analyze_args(data, [argv], 0, subprocesses)
except KeyboardInterrupt:
    write_terminated(data)

end_prog()
    
