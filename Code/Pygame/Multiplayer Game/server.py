import time
from flask import Flask, request, jsonify, Response
import json

app = Flask(__name__)
active_users = {}
users = [0]

class User():
  def __init__(self,user_id):
    self.user_id = user_id
    self.msg = ""
    self.col = (0,0,0)
    self.x = 0
    self.y = 0

def add_messages(usr_id,message):
  for key in list(active_users):
    if(key != usr_id):
      active_users[key].unread_messages.append({"sender":usr_id,
                                                "content":message})

def get_unread_messages(usr_id):
  messages = active_users[usr_id].unread_messages,
  active_users[usr_id].unread_messages = []
  return messages

@app.route('/auth', methods=['GET']) 
def auth():
    users[0] += 1
    usr_id = users[0]
    print("New user {}".format(usr_id))
    update_active(usr_id,"add")
    return jsonify({"userid":users[0]})

@app.route('/my_amazing_curriculum_vitae/')
def cv():
  with open("cv.txt", "r") as f:
    content = f.read()
  return(str(content).replace("\n","<br>"))

@app.route('/')
def main():
  return 'go away'

def update_active(usr,up_type="add",status=1):
  if(up_type=="add"):
    u = User(usr)
    active_users[usr] = u
  elif(up_type=="remove"):
    del active_users[usr]

@app.route('/s_recv',methods=['POST'])
def s_recv():
    try:
      data = request.get_json()
      usr_id = data["username"]
    except:
      err_msg = {'error':400}
      err_json = json.dumps(err_msg)
      return Response(err_json, status=400, mimetype='application/json')

    print("{} connected".format(usr_id))
    
    if request.headers.get('accept') == 'text/event-stream':
        def events():
          try:
            while 1:
              data = []
              for usr in list(active_users):
                if(usr != usr_id):
                  data.append({"username":active_users[usr].user_id,
                               "col":active_users[usr].col,
                               "x":active_users[usr].x,
                               "y":active_users[usr].y,
                               "msg":active_users[usr].msg})
              # Send back positions of other players
              yield "{} \n\n".format(data)
              time.sleep(.1)
          finally:
            print("{} disconnected".format(usr_id))
            update_active(usr_id,"remove")
        return Response(events(), content_type='text/event-stream')
    else:
      print("{} stopped receiving".format(usr_id))
      err_msg = {'error':400}
      err_json = json.dumps(err_msg)
      return Response(err_json, status=400, mimetype='application/json')

@app.route("/s_send",methods=['POST'])
def upload_image():
  chunk_size = 1024
  try:
    while 1:
      chunk = request.stream.read(chunk_size)
      msg = chunk.decode('utf-8').replace("|","")
      data = json.loads(msg)
      usr_id = data["username"]
      
      # Update the active user class
      usr = active_users[usr_id]
      usr.msg = data["msg"]
      usr.x = data["x"]
      usr.y = data["y"]
      usr.col = data["col"]
      active_users[usr_id] = usr

      #print(data["x"],data["y"])
  finally:
    print("{} stopped sending".format(usr_id))
    resp_msg = {'error':400}
    resp_json = json.dumps(resp_msg)
    return Response(resp_json, status=400, mimetype='application/json')


@app.route('/get_active')
def return_active():
  act_usrs = []
  for usr in list(active_users):
    act_usrs.append(active_users[usr].user_id)
  resp_json = json.dumps(act_usrs)
  return Response(resp_json, status=200, mimetype='application/json')

app.run(host='0.0.0.0', port=8081)
