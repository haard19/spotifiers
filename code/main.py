from flask import Flask
import json
from feature_prep import Prepare

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()