#!/usr/bin/python3


import redis
import subprocess as sb
import os
import pyroute2 as pr2


def get_current_vlans(master):
    lans = []
    for lan in os.listdir('/sys/class/net'):
        if lan.count(master + '.'):
            lans += [lan]
    return lans


def build_vlan(master, index):
    return master + '.' + index


def add_VLAN(master, index):
    return sb.run(['sudo', 'vconfig', 'add', master, index])


def del_VLAN(vlan):
    sb.run(['sudo', 'vconfig', 'rem', vlan])


def set_admin_state(inter, state):
    print(inter)
    return sb.run(['sudo', 'ip', 'link', 'set', 'dev', inter, state])


def del_vlans(INDEXES, lans):
    vlans = set(map(lambda index: build_vlan(MASTER, index), INDEXES))
    need_to_del = set(lans) ^ vlans & set(lans)
    
    for vlan in need_to_del:
        del_VLAN(vlan)
    


def get_operstate(vlan):
    return pr2.IPDB().interfaces[vlan]['state']


def parse_state(state: str):
    return 'up' if int(state) else 'down'


def work():
    if INDEXES:
        for index in INDEXES:
            vlan = MASTER + '.' + index
            add_VLAN(MASTER, index)

        for vlan in ADMIN_STATE:
            state = ADMIN_STATE[vlan]

            state = parse_state(state)

            set_admin_state(vlan, state)
            OPER_STATE[vlan] = get_operstate(vlan)


r = redis.Redis(decode_responses=True)

MASTER = r.get('master')
INDEXES = r.lrange('vlans', '0', '-1')
ADMIN_STATE = {key: r.hget('admin-state', key) for key in r.hkeys('admin-state')}
OPER_STATE = dict()
lans = get_current_vlans(MASTER)

del_vlans(INDEXES, lans)
work()

if OPER_STATE:
    r.hset('oper-state', mapping=OPER_STATE)


