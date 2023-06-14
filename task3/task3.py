#!/usr/bin/python3


import argparse as ap
import sys
import os
import json


parser = ap.ArgumentParser()

parser.add_argument('-P', '--pid', action='store_true')
parser.add_argument('-u', '--uid', action='store_true')
parser.add_argument('-g','--gid', action='store_true')
parser.add_argument('-e','--env', nargs='*', required=True, action='append')
parser.add_argument('-d','--dir', nargs=1, required=True)
parser.add_argument('-p','--pos', nargs='+', required=True, action='append')
parser.add_argument('-f','--file', nargs=1, required=True)

args = parser.parse_args()

data = dict()

if args.pid != None:
    data['pid'] = os.getpid()
    
if args.uid != None:
    data['uid'] = os.getuid()
    
if args.gid != None:
    data['gid'] = os.getgid()
    
if args.env != None:
    data['env'] = dict()
    try:
        for var in args.env:
            data['env'][var[0]] = os.environ[var[0]]
    except KeyError:
        print(f'var {var[0]} had not found')
        
if args.dir != None:
    data['dir'] = os.listdir()
    
if args.pos != None:
    indexes, values, pos_args = [], [], []
    
    for i in args.pos:
        indexes += [int(i[0])]
        pos_args += i[1:len(i)]
    for i in indexes:
        try:
            values += [pos_args[i]]
        except IndexError:
            pass
    data['pos'] = values
    
if args.file[0] == '-':
    data['file'] = sys.stdin.readline()
    
else:
    try:
        with open(args.file[0], "r") as file:
            data['file'] = file.readlines()
    except FileNotFoundError:
        data['file'] = 'Not found'
        print(f'file {args.file[0]} not found')
        
print(json.dumps(data, indent=True))
