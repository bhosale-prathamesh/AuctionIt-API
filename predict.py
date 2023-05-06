from flask import Flask
import tensorflow as tf
import os
from flask import request
import json
from model import train

app = Flask(__name__)

@app.route("/")
def predict():
    user_id = request.args.get('user_id', type = str)

    print(user_id)
    path = os.path.join(os.getcwd(),"model_v1")

    loaded = tf.keras.models.load_model(path)

    scores, titles = loaded([str(user_id)])
    
    l = list(map(str,titles[0].numpy()))
    l = [x[2:-1] for x in l]
    jsonStr = json.dumps(l)
    return jsonStr

@app.route("/update")
def update_model():
    return train()
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)