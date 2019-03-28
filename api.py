from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'hosts_mac'
app.config['MONGO_URI'] = 'mongodb://0.0.0.0:27017/hosts_mac'

mongo = PyMongo(app)

@app.route('/active', methods=['GET'])
def get_active_hosts():
  cur = mongo.db.posts.find().sort('_id', -1).limit(1)
  output = []
  for s in cur:
    for h in s['hosts']:
        output.append({'name' : h['name'], 'time' : h['time']})
  return jsonify({'result' : output})

@app.route('/timeline', methods=['GET'])
def get_timeline_hosts():
  cur = mongo.db.posts.find()
  hosts = []
  output = []
  for s in cur:
    for h in s['hosts']:
        output.append({'name' : h['name'], 'time' : h['time']})
    hosts.append(output)
    output = []
  return jsonify({'result' : hosts})

if __name__ == '__main__':
    app.run(debug=True)
