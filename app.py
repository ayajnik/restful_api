## importing modules
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float
import os
from flask_marshmallow import Marshmallow

# initializing the app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///" + os.path.join(basedir,"planets.db")

db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database created")


@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("Dropping the database")


@app.cli.command("db_seed")
def db_seed():

    mercury = Planets(planet_name = "Mercury",
                    planet_type = "Type D",
                    home_star = "Sol",
                    mass = 3.258e23,
                    radius = 1516,
                    distance = 3598e6
                    )

    venus = Planets(planet_name = "Venus",
                    planet_type = "Type D",
                    home_star = "Sol",
                    mass = 3.258e24,
                    radius = 1517,
                    distance = 3598e6
                    )

    earth = Planets(planet_name = "Earth",
                    planet_type = "Type M",
                    home_star = "Sol",
                    mass = 3.258e25,
                    radius = 1518,
                    distance = 3698e6
                    )

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(
                    first_name = "Ayush",
                    last_name = "Yajnik",
                    email = "test@test.com",
                    password = "Password@123"
                    )
    
    db.session.add(test_user)
    db.session.commit()
    print("Database seeded")

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

@app.route("/planets")
def planets():
    planets_list = Planets.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(data = result)


## creating the ORM template for the database
class User(db.Model):

    __tablename__ = "users"
    id = Column(Integer)
    first_name = Column(String, primary_key = True)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    

@app.route('/add_user',methods = ['POST'])
def add_user():
    email = request.form['email']
    testing_email = User.query.filter_by(email = 'email').first()
    if testing_email:
        return jsonify(message = 'This user already exists')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        user = User(first_name = first_name, last_name = last_name, email = email, password = password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="The user has been added")
class Planets(db.Model):

    __tablename__ = "name"
    planet_id = Column(Integer, primary_key = True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    distance = Column(Float)
    radius = Column(Float)


class UserSchema(ma.Schema):
    class Meta():
        fields = ("id", "first_name", "last_name", "email", "password")


class PlanetSchema(ma.Schema):
    class Meta():
        fields = ("planet_id", "planet_name", "planet_type", "home_star", "mass","distance", "radius")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)
    



if __name__ == "__main__":
    app.run()