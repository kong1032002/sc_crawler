import json
from flask import Flask
from libs.data_preprocession import *

app = Flask(__name__)
@app.route('/')
def index():
    return json.dumps({
        'name': 'alice',
        'email': 'alice@outlook.com'
    })
    
@app.route('/predict/pair/<string:id>')
def predict(id):
    result = preprocessing(early_predict=7, pair_id=id)
    return result

@app.route('/early_predict/pair/<int:id>')
def early_predict(id):
    return f'Pair ID: {id}'

app.run()