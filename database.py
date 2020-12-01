#CODER @Sigaris
#Database
import os , json

if not os.path.exists('db.json'):
    with open('db.json', 'w') as saves:
        data = {"info-self":{
            "api_id": [],
            "api_hash": [],
            },
            "list":{
            "user": []
            }
                }
        json.dump(data, saves)

with open("db.json", "r") as f:
    DATA = json.load(f)

def save():
    global DATA
    with open("db.json", "w+") as f:
        json.dump(DATA, f)
