#!/usr/bin/python3


import subprocess as sb
import sys


master = sys.argv[-2]
index = sys.argv[-1]
sb.run(['sudo', 'vconfig', 'add', master, index], stdout=None)
