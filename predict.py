from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import tensorflow as tf
import os
from bson.json_util import dumps
from flask import request
from flask_cors import CORS
import json
from model import train
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
CORS(app)

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://adarsh:adarsh9325268690@auctioncluster.y5iau8c.mongodb.net/?retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['test']

@app.route("/")
def predict():
    user_id = request.args.get('user_id', type = str)

    path = os.path.join(os.getcwd(),"model_v1")

    loaded = tf.keras.models.load_model(path)

    scores, titles = loaded([str(user_id)])
    
    l = list(map(str,titles[0].numpy()))
    l = [x[2:-1] for x in l]
    dbname = get_database()
    collection_name = dbname['ads']
    f = []
    for id in l:
        item = list(collection_name.find({"_id":ObjectId(id)}))[0]
        if not item['auctionEnded']:
            item['_id'] = str(item['_id'])
            item['owner'] = str(item['owner'])
            item['room'] = str(item['room'])
            item['createdAt'] = str(item['createdAt'])
            item['updatedAt'] = str(item['updatedAt'])
            f.append(item)
    new_ads = list(collection_name.find())[::-1]
    for i in new_ads:
        if (str(i["_id"]) not in l) and (not i['auctionEnded']):
            i['_id'] = (i['_id'])
            i['owner'] = str(i['owner'])
            i['room'] = str(i['room'])
            i['createdAt'] = str(i['createdAt'])
            i['updatedAt'] = str(i['updatedAt'])
            f.append(i)
    
    jsonStr = dumps(f)
    return jsonStr

@app.route("/update")
def update_model():
    return train()
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)