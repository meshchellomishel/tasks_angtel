#!/usr/bin/python3


import redis
import pyroute2 as pr2
import hashlib


def parse_mes(mes: str) -> str:
    return mes.split('-')[-1]


def get_channel_mes(ip: str) -> str:
    return f'neigh-{ip}'


def get_table_hash(table: dict) -> str:
    return hashlib.sha256(str(table).encode()).hexdigest()


def parse_ARP(data: list) -> dict:
    table = {i['attrs'][0][1]: i['attrs'][1][1] for i in data}
    return table


def change_value(r: redis.Redis, key: str, table: dict):
    if key in table:
        r.hset(TABLE_NAME, key, table[key])
    else:
        r.hdel(TABLE_NAME, key)


def check_changes(prev_table_hash: str, ipr: pr2.IPRoute):
    new_table = parse_ARP(ipr.neigh('dump'))
    new_table_hash = hashlib.sha256(str(new_table).encode()).hexdigest()

    if new_table_hash != prev_table_hash:
        return new_table


def print_changes(changes: list, prev_keys: set):
    for ip in changes:
        if ip in prev_keys:
            print(f'Changing: del {ip}')
        else:
            print(f'Changing: add {ip}')


def get_changes(prev_table: dict, new_table: dict) -> list:
    prev_keys = set(prev_table.keys())
    new_keys = set(new_table.keys())

    changes = []
    changes += list(prev_keys ^ new_keys)

    print_changes(changes, prev_keys)

    for key in new_keys:
        if key in prev_keys:
            if new_table[key] != prev_table[key]:
                changes += [key]
                print(f'Changing: set {key}')

    return changes


def send_mes(ip: str, r: redis.Redis):
    print(f'--> publish: neigh-{ip}')
    r.publish(CHANNEL_NAME, get_channel_mes(ip))


def change(r: redis.Redis, prev_table: dict, table: dict):
    changes = get_changes(prev_table, table)

    for ip in changes:
        send_mes(ip, r)
        change_value(r, ip, table)


def work(ipr: pr2.IPRoute, r: redis.Redis):
    table = parse_ARP(ipr.neigh('dump'))
    table_hash = get_table_hash(table)

    while 1:
        res = check_changes(table_hash, ipr)

        if res:
            prev_table, table = table, res
            table_hash = get_table_hash(table)

            change(r, prev_table, table)


def start():
    ipr = pr2.IPRoute()
    r = redis.Redis()

    work(ipr, r)


CHANNEL_NAME = 'state-change'
TABLE_NAME = 'neigh-state'

try:
    start()
except KeyboardInterrupt:
    print('program stopped')