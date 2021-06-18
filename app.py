## importing modules
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message


# initializing the app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///" + os.path.join(basedir,"planets.db")
app.config['JWT_SECRET_KEY'] = 'super-secret'
##register to mail trap and get the credentials from integrations section
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '06770af9465fc0'
app.config['MAIL_PASSWORD'] = '266b2b0e01c6d1'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


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

@app.route('/login', methods = ['POST'])
def user_login():
    if request.is_json():

        email = request.json['email']
        password = request.json['password']
        testing_email = User.query.filter_by(email = email).first()

    else:

        email = request.form['email']
        password = request.form['password']

    test =  User.query.filter_by(email = 'email',password=password).first()
    if test:
        access_token = create_access_token(email=email)
        return jsonify(message = "Login succesfull")
    else:
        return jsonify(message = "Bad credentials")


@app.route('/forgot_password', methods = ['GET'])
def forgot_password():
    email = request.args.get('email')
    test = User.query.filter_by(email = email).first()
    if test:
        msg = Message("Your password is "+test.password, sender = "test@test.com", recipients = ['ayushyajnik2@gmail.com'])
        mail.send(msg)
    else:
        return jsonify(message = 'Enter another email address')

##retrieving the data 
@app.route('/planet_data/<int:planet_id>', methods=['GET'])
def planet_data(planet_id = int):
    planet = Planets.query.filter_by(planet_id=planet_id).first()
    
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result.data)
    else:
        return jsonify(message="Planet not found")


##adding new records
@app.route('/add_planet', methods=['POST'])
def add_planet():
    planet_name = request.form['planet_name']
    test = Planets.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify(message="There is already a planet entered by this name.")
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['form'])
        distance = float(request.form['distance'])
        radius = float(request.form['radius'])

        new_planet = Planets(
            planet_name = planet_name
            ,planet_type = planet_type
            ,home_star = home_star
            ,mass = mass
            ,distance = distance
            ,radius = radius
        )

        db.session.add(new_planet)
        db.session.add()

        return jsonify(message="New planet added")
        




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