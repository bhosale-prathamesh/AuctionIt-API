from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import tensorflow as tf
import os
from flask import request
from flask_cors import CORS
import json
from model import train

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
        item = list(collection_name.find({"_id":ObjectId(id)}))
        if not item[0]['auctionEnded']:
            f.append(item[0])
    new_ads = list(collection_name.find())[::-1]
    for i in new_ads:
        if i not in l:
            f.append(i)
    jsonStr = json.dumps(f,default=str)
    return jsonStr

@app.route("/update")
def update_model():
    return train()
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)