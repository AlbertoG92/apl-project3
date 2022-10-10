from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps
import uuid
import jwt
import datetime

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/appdb'
app.config['SECRET_KEY']="'b'\x9bVn\xab\xdf\xf9\x98\x1b\xe2i]\xc4\xea\xa1\xf7\xd1\x08\xb8\xbf\xf8\x01\xe9\x0f\xb4''"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255))


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(public_id=data['public_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator

@app.route('/register', methods=['POST'])
def signup_user(): 
   data = request.get_json() 
   hashed_password = generate_password_hash(data['password'], method='sha256')
 
   new_user = User(id=str(uuid.uuid4()), email=data['email'], username=data['username'], password=hashed_password)
   db.session.add(new_user) 
   db.session.commit()   
   return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['POST']) 
def login_user():
   auth = request.authorization  
   if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'login required"'})   
 
   user = User.query.filter_by(username=auth.username).first()  
   if check_password_hash(user.password, auth.password):
       token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
 
       return jsonify({'token' : token})
 
   return make_response('could not verify',  401, {'Authentication': '"login required"'})


@app.route('/users', methods=['GET'])
@token_required
def get_all_users(): 
   users = User.query.all()
   result = []  
   for user in users:  
       user_data = {}  
       user_data['email'] = user.email 
       user_data['username'] = user.username
     
       result.append(user_data)  
   return jsonify({'users': result})

