#!/usr/bin/python3


import redis


r = redis.Redis()
r.set('master', 'enp0s3')
r.lpush('vlans', '10', '20')
r.hset('admin-state', mapping={'enp0s3.10': '1', 'enp0s3.20': '0'})

