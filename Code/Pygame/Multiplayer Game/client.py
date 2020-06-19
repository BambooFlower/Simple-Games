from requests import session, exceptions
import ssl
from multiprocessing import Process, freeze_support, Queue, Manager
import json
import time
from window import Game


def get_updates(s,myid,global_list):
    data = {"username":myid}
    server = "https://server---5.repl.co/{}"
    while(True):
        time.sleep(1)
        data["username"] = myid
        data_json = json.dumps(data)
        try:
            r = s.post(server.format("getupdates"),data=data_json,timeout=0.1)
            if(r.json() != []):
                print(r.json())
                #global_list.append(r.json())
                global_list[0] = r.json()
        except exceptions.ConnectionError:
            pass
        except KeyboardInterrupt:
            break

        
if __name__ == '__main__':
    # Create session
    s = session()
    # Set Content-Type header
    s.headers["Content-Type"] = "application/json"
    
    server = "https://server---5.repl.co/{}"
    data = {}
    data_json = json.dumps(data)

    # Authenticate    
    endpoint = "auth"    
    r = s.get(server.format(endpoint))
    myid = r.json()["userid"]
    print("myid={}".format(myid))
    
    manager = Manager()
    global_list = manager.dict()
    
    # Create a child process to listen for incoming updates
    freeze_support()
    p = Process(target=get_updates,args=(s,myid,global_list,)).start()
    
    g = Game(myid,s)
    g.loop()
    p.terminate()
    
