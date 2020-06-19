#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:26:39 2020
"""

from multiprocessing import Process, Pipe
import time

class Child():
    def __init__(self,p):
        self.p_out,self.p_in = p
        self.curr = 0

    def loop(self):
        i = 0
        while 1:
            if self.p_out.poll():
                self.curr = self.p_out.recv()            
            print(self.curr,i)
            time.sleep(1)
            if(i>10):
                break
            i+=1
    
class Parent():
    def __init__(self):
        p_out, p_in = Pipe()
        child = Child((p_out,p_in))
        self.p_out,self.p_in = p_out,p_in
        updater = Process(target=child.loop)
        updater.daemon = True
        updater.start()
    def send_new(self,val):
        self.p_in.send(val)
    
p = Parent()

for i in range(1000):
    p.send_new({1:i})
