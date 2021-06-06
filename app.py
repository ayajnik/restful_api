## importing modules
from flask import Flask, jsonify, request
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import Column, String, Integer, Float
import os

# initializing the app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =   "sqllite:///" + os.apth.join(basedir,"planets.db")


# creating endpoint for index page
@app.route("/")
def index():
    return "hello world", 200

#end point for page not found
@app.route("/new_page")
def not_found():
    return "Page not found", 404

#url parameter - age testing
@app.route("/parameter")
def parameters():
    name = request.args.get("name")
    age = int(request.args.get("age"))

    if age > 18:
        return jsonify(message="Welcome " + name + " .You are welcomed."),200
    else:
        if age < 18:
            return jsonify(message="Sorry " + name + " you are not welcomed"), 401

##modern day for passing parameters
@app.route("/url_varibles/<string:name>/<int:age>")
def url_variables(name:str,age:int):
    name = request.args.get("name")
    age = int(request.args.get("age"))

    if age > 18:
        return jsonify(message="Welcome " + name + " .You are welcomed."),200
    else:
        if age < 18:
            return jsonify(message="Sorry " + name + " you are not welcomed"), 401





if __name__ == "__main__":
    app.run()