import pymongo
from flask import Flask,jsonify,render_template,request
from flask_pymongo import PyMongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://admin:AAGzez02811@10.100.2.126:27017")
#client = pymongo.MongoClient("mongodb://admin:AAGzez02811@node9149-advweb-11.app.ruk-com.cloud:11154")

db = client["MMORPG"]


####### index ###############
@app.route("/")
def index():
    texts = "Hello World , Welcome to MongoDB"
    return texts

########## GET ALL #################
@app.route("/Character", methods=['GET'])
def get_allcharacter():
    char = db.Character
    weapon = db.Weapon
    output = []
    output2 = []
    for x in char.find():
        output.append("Character : " + {'name' : x['name'],'level' : x['level'],
                        'class' : x['class'],
                        'guild' : x['guild'],
                        'server' : x['server']})

    
    for y in weapon.find():
        output.append("Weapon : " + {'weapon_name' : y['weapon_name'],'weapon_type' : y['weapon_type'],
                        'weapon_amount' : y['weapon_amount']})
    return jsonify(output)

############## GET ONE ############################
@app.route("/Character/<name>", methods=['GET'])
def get_onecharacter(name):
    char = db.Character
    x = char.find_one({'name' : name})
    if x:
        output = {'name' : x['name'],'level' : x['level'],
                        'class' : x['class'],
                        'guild' : x['guild'],
                        'server' : x['server']}
    else:
        output = "No such name"
    return jsonify(output)

######################### INSERT ####################
@app.route('/Character', methods=['POST'])
def add_character():
  char = db.Character
  name = request.json['name']
  level = request.json['level']
  classes = request.json['class']
  guild = request.json['guild']
  server = request.json['server']
  
  char_id = char.insert({'name': name, 'level': level,
                        'class': classes,
                        'guild': guild,
                        'server': server})
  new_char = char.find_one({'_id': char_id })
  output = {'name' : new_char['name'], 'level' : new_char['level'],
                        'class' : new_char['class'],
                        'guild' : new_char['guild'],
                        'server' : new_char['server'],}
  return jsonify(output)

##################### UPDATE ########################
@app.route('/Character/<name>', methods=['PUT'])
def update_character(name):
    char = db.Character
    x = char.find_one({'name' : name})
    if x:
        myquery = {'name' : x['name'],'level' : x['level'],
                        'class' : x['class'],
                        'guild' : x['guild'],
                        'server' : x['server']}

    name = request.json['name']
    level = request.json['level']
    classes = request.json['class']
    guild = request.json['guild']
    server = request.json['server']
    
    newvalues = {"$set" : {'name' : name, 'level' : level,
                        'class' : classes,
                        'guild' : guild,
                        'server' : server,}}

    char_id = char.update_one(myquery, newvalues)

    output = {'name' : name, 'level' : level,
                        'class' : classes,
                        'guild' : guild,
                        'server' : server}

    return jsonify(output)

##################### DELETE ############################ 
@app.route('/Character/<name>', methods=['DELETE'])
def delete_character(name):
    char = db.Character
    x = char.find_one({'name' : name})

    char_id = char.delete_one(x)

    output = "Deleted complete"

    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 80)