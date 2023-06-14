#!/usr/bin/python3


import signal
import time
import sys
import os
import subprocess as sb
from pprint import pprint


def end_prog():
    pprint(data)


def run_proc(args, IS_RUNNING, In=None, out=None, text=True):
    print(f'running\nin={In}\nout={out}')
    
    pr = sb.Popen(args, stdin=In, stdout=out, text=text)
    IS_RUNNING = True
    pr.wait()

    print('finished')
    IS_RUNNING = False
    pr = None
    

def handler(sig_num, frame):
    end_prog()
    print(IS_RUNNING, pr)
    if IS_RUNNING:
        pr.send_signal(sig_num)
    sys.exit()


def check_file(args):
    try:
        return args[-2] == "<"
    except IndexError:
        return False


def analyze_args(argv, index, IS_RUNNING, stdin, stdout):
    if index != len(argv):
        args = argv[index].split()
        print(args)
        
        if check_file(args):
            subproc = args[0:len(args)-2]
            
            with open(args[-1], "w+") as file:
                run_proc(subproc, IS_RUNNING, In=stdin, out=file)
                stdin, stdout = file, None
                analyze_args(argv, index + 1, IS_RUNNING, stdin, stdout)

        else:
            with open('buf.txt', "r+") as file:
                run_proc(args, IS_RUNNING, In=stdin, out=file)
                stdin, stdout = file, None
                analyze_args(argv, index + 1, IS_RUNNING, stdin, stdout)
        
        return stdin, stdout


IS_RUNNING = False
pr = None

argv = sys.argv
argv = " ".join(argv[1:len(argv)])

signal.signal(signal.SIGUSR1, handler)

data = dict()
stdin, stdout = None, None

try:
    if argv.count('|') != 0:
        argv = argv.split('|')

        analyze_args(argv, 0, IS_RUNNING, stdin, stdout)
    else:
        analyze_args([argv], 0, IS_RUNNING, stdin, stdout)
except KeyboardInterrupt:
    end_prog()
    
