#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:13:50 2020
"""

from requests import session,exceptions
import json
import time

url = "https://server---5.repl.co/{}"

s_send = session()
s_recv = session()
# Set Content-Type header
s_send.headers["Content-Type"] = "application/json"
s_send.headers["Transfer-Encoding"] = None#"chunked"

s_recv.headers["Content-Type"] = "application/json"
s_recv.headers["accept"] = "text/event-stream"

def get_id():  
    # Authenticate    
    endpoint = "auth"    
    r = s_recv.get(url.format(endpoint))
    #print(r)
    if(r.status_code == 200):
        myid = r.json()["userid"]
        return myid
    else:
        raise exceptions.ConnectionError

myid = get_id()
if(myid == -1):
    raise 

def get_updates():
    data = {"username":myid}
    r=s_recv.post(url.format('s_recv'),data=json.dumps(data),stream=True)
    for line in r.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(myid,decoded_line)

def inf_seq():
    i = 0
    while 1:
        msg = {"username":myid,
               "pos":(0,0),
               "msg":"{}".format(i),
               "col":(0,0,0)}
        msg = json.dumps(msg)
        msg = msg.ljust(1024,"|")
        yield msg
        time.sleep(0.1)
        #print(msg)
        i += 1
            
def send_updates():
    s_send.post(url.format("s_send"),data=inf_seq(),stream=True)

get_updates()
send_updates()
