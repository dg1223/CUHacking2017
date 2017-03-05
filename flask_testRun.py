import flask
from flask import Flask
app = Flask(__name__)

@app.route('/data/')
def home():
    resp = flask.jsonify({"text":"Hello"})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
#def hello():
#    resp = flask.Response("Hello World!")
#    resp.headers['Access-Control-Allow-Origin'] = '*'
#    return resp

if __name__ == "__main__":
    app.run(debug = True)