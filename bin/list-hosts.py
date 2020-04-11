#!/home/justin/.pyenv/shims/python

import redis

r = redis.Redis(host="www.paladiamors.com", db=0)
for key in r.scan_iter("*"):
    print(key.decode("utf8"), r.get(key).decode("utf8"))
