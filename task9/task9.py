#!/usr/bin/python3


import redis
import subprocess as sb
import os


def add_VLAN(master, index):
    return sb.run(['sudo', 'vconfig', 'add', master, index])


def set_admin_state(inter, state):
    print(inter)
    return sb.run(['sudo', 'ip', 'link', 'set', 'dev', inter, state])


def filter(VLANS, lans):
    res = []
    for lan in VLANS:
        if not lan in lans:
            res += [lan]
        elif DELETE_COLISIONS:
            sb.run(['sudo', 'vconfig', 'rem', lan])
    return res


def get_operstate(vlan):
    with open(f'/sys/class/net/{vlan}/operstate', 'r') as file:
        return file.readlines()


def parse_state(state: str):
    return 'up' if int(state) else 'down'


def work():
    if VLANS:
        for index in VLANS:
            vlan = MASTER + '.' + index
            add_VLAN(MASTER, index)

        for vlan in ADMIN_STATE:
            state = ADMIN_STATE[vlan]

            state = parse_state(state)

            set_admin_state(vlan, state)
            OPER_STATE[vlan] = get_operstate(vlan)[0].split('\n')[0]


r = redis.Redis(decode_responses=True)

MASTER = r.get('master')
VLANS = r.lrange('vlans', '0', '-1')
ADMIN_STATE = {key: r.hget('admin-state', key) for key in r.hkeys('admin-state')}
DELETE_COLISIONS = bool(r.get('deletecolisions'))
OPER_STATE = dict()
lans = os.listdir('/sys/class/net')
VLANS = filter(VLANS, lans)

work()

r.hset('oper-state', mapping=OPER_STATE)


