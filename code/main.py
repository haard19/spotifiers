from flask import Flask, request
import json
from feature_prep import Prepare
from model import Model

app = Flask(__name__)

mod = Model()

@app.route("/prepare")
def prepare():
    prep = Prepare()
    prep.prep()
    data = {
        "msg": "Features prepared."
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/train")
def train():
    ratio = int(request.args.get("ratio"))
    model = request.args.get("model")
    mod.train(ratio, model)
    data = {
        "msg": f"Model ({model}) trained."
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/recommend")
def recommend():
    data = mod.recommend()
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run()