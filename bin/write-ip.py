#!/home/justin/.pyenv/shims/python
# Script to write ip to the redis server

import redis
import netifaces as ni

r = redis.Redis(host="www.paladiamors.com", db=0)
host_ip = ni.ifaddresses('enp3s0')[ni.AF_INET][0]['addr']

r.set("Halcyon99", host_ip)
