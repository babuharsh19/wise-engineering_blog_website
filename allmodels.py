from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import loginmanager,app
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.ext.declarative import declarative_base
import json

with open('config.json','r') as f:
    parameter = json.load(f)["parameters"]

local_server = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['local_uri']
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_uri']

app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)
Migrate(app,db)
Base = declarative_base()

    
class Contacts(db.Model):

    '''sno, name, email, phone num, message, date'''

    sno = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    
    # def __init__(self,name,email,phone_no,message):
    #     name=self.name
    #     email=self.email
    #     phone_no=self.phone_no
    #     message = self.message

    def __repr__(self):
        return '<name>{}'.format(self.name)

class Post(db.Model):

    sno = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    subheading = db.Column(db.String(200), nullable=False)  
    slug = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(800), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    img_file = db.Column(db.String(20), nullable=False)
    
    def __init__(self,sno,title,slug):
        sno=self.sno
        title=self.title
        slug=self.slug
    def __repr__(self):
        return '<sno>{},<title>{}'.format(self.sno,self.title)

class Users(db.Model,UserMixin):

    '''sno, name, email, phone num, message, date'''

    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=False)  
    password = db.Column(db.String(20), nullable=False)
    #password_hash = db.Column(db.String(20), nullable=False)

    def __init__(self,user_id,name,email,password):
        user_id=self.user_id
        name=self.name
        email=self.email
        password=self.password
        
    # def check_password(self,password):
    #     check_password_hash(self.password_hash,password)
    def __repr__(self,name):
        return '<name>{}'.format(self.name)

class Admin(db.Model,UserMixin):

    email = db.Column(db.String(200), nullable=False,primary_key=True)  
    password = db.Column(db.String(20), nullable=False)

    def __init__(self,email,password):
            email=self.email
            password=self.password
            #password_hash = self.generate_password_hash(password)

    def check_password(self,password):
            check_password_hash(self.password_hash,password)

    def __repr__(self,email):
            return '<email>{}'.format(self.email)


@loginmanager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)