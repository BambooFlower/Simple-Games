#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from random import randint
import json
from requests import session,exceptions
import time
from multiprocessing import Process, freeze_support, Pipe

class Network():
    def __init__(self,p,myid=-1):   
        self.p_out,self.p_in = p
        self.s_send = session()
        self.s_recv = session()
        self.url = "https://server---5.repl.co/{}"
        # Set Content-Type header
        self.s_send.headers["Content-Type"] = "application/json"
        self.s_send.headers["Transfer-Encoding"] = None
        
        self.s_recv.headers["Content-Type"] = "application/json"
        self.s_recv.headers["accept"] = "text/event-stream"
                                
        if(myid == -1):
            self.myid = self.get_id()
            #self.process_type = "send"
        else:
            self.myid = myid
            #self.process_type = "recv"
  
        self.send_data = {"username":self.myid,
                  "msg":"",
                  "x":-100,
                  "y":-100,
                  "col":(0,0,0)}
        
    def get_id(self):  
        # Authenticate    
        endpoint = "auth"    
        r = self.s_recv.get(self.url.format(endpoint))
        #print(r)
        if(r.status_code == 200):
            myid = r.json()["userid"]
            return myid
        else:
            raise exceptions.ConnectionError("Server is down :(")
            
    def inf_seq(self):
        #i = 0
        while 1:
            try:
                if self.p_out.poll():
                    self.send_data = self.p_out.recv()
                msg = json.dumps(self.send_data)
                msg = msg.ljust(512,"|")
                yield msg
                time.sleep(0.1)
                #print(msg)
                #i += 1
            except KeyboardInterrupt:
                print("Stopped sending")
                break
         
    def send_updates(self):
        self.s_send.post(self.url.format("s_send"),data=self.inf_seq(),
                                                     stream=True)
        
    def get_updates(self):
        data = {"username":self.myid}
        r=self.s_recv.post(self.url.format('s_recv'),data=json.dumps(data),
                      stream=True)
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                #print(self.myid,decoded_line)
                self.p_in.send(decoded_line)

class Game():
    def __init__(self):
        freeze_support()
        send_out, send_input = Pipe()
        recv_out, recv_input = Pipe()
                
        self.send_list = (send_out,send_input)
        self.recv_list = (recv_out,recv_input)
        
        n1 = Network(self.send_list)
        self.myid = n1.myid
        n2 = Network(self.recv_list,self.myid)
        
        # Start sending process
        self.send_p = Process(target=n1.send_updates)
        self.send_p.start()
        
        
        # Start receiving process
        self.recv_p = Process(target=n2.get_updates)
        self.recv_p.start()
        
        
        pygame.init()

        self.win = pygame.display.set_mode((480,480))
        self.p_x = randint(100,400)
        self.p_y = randint(100,400)
        self.p_width = 40
        self.p_height = 40
        self.p_vel = 0.7
        self.p_col = (randint(0,255),
                      randint(0,255),
                      randint(0,255))
        
        self.recv_data = []
   
    def draw_others(self):
        for d in self.recv_data:
            #print(d)
            pygame.draw.rect(self.win,tuple(d["col"]),
                         (d["x"],d["y"],
                          self.p_width,self.p_height))
    
    def loop(self):
        clock = pygame.time.Clock()
        run = True
        time_last = time.time()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send_p.terminate()
                    self.send_p.join()
                    self.recv_p.terminate()
                    self.recv_p.join()
                    run = False
            
            keys = pygame.key.get_pressed()
            
            dt = clock.tick(60)
    
            if keys[pygame.K_LEFT]:
                self.p_x -= int(self.p_vel*dt)
            if keys[pygame.K_RIGHT]:
                self.p_x += int(self.p_vel*dt)
            if keys[pygame.K_UP]:
                self.p_y -= int(self.p_vel*dt)
            if keys[pygame.K_DOWN]:
                self.p_y += int(self.p_vel*dt)
            
            send_data = {"username":self.myid,
                  "msg":"",
                  "x":self.p_x,
                  "y":self.p_y,
                  "col":self.p_col}

            if(time.time() - time_last > 0.1):
                self.send_list[1].send(send_data)
                time_last = time.time()
                
            if self.recv_list[0].poll():
                self.recv_data = eval(self.recv_list[0].recv())
                #print(self.recv_data,"\n\n ")
                
            self.win.fill((0,0,0))
            self.draw_others()
            pygame.draw.rect(self.win,self.p_col,
                             (self.p_x,self.p_y,
                              self.p_width,self.p_height))
            pygame.display.update()
        pygame.quit()

if __name__ =="__main__":
    g = Game()
    g.loop()