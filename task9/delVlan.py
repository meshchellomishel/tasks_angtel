#!/usr/bin/python3


import subprocess as sb
import sys


vlan = sys.argv[-1]
sb.run(['sudo', 'vconfig', 'rem', vlan], stdout=None)
