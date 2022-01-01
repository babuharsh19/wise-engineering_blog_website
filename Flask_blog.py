from flask import Flask, render_template, request,url_for,Blueprint,flash
from allmodels import Contact,Posts,app,db
import pymysql
import json
from flask_mail import Mail
from flask_login import login_user, logout_user, login_required

user = Blueprint('core',__name__)

with open('config.json','r') as f:
    parameter = json.load(f)["parameters"]

local_server = True
app.config.update(
    MAIL_SERVER ='smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = parameter['gmail_id'],                                                                       
    MAIL_PASSWORD = parameter['gmail_password']
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_uri']
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route("/home")
@login_required
def home():
    posts = Posts.query.filter_by().all()[0:3]
    return render_template("index.html",param=parameter,posts=posts)

@app.route("/about")
@login_required
def about():
    return render_template('about.html',param=parameter)

@app.route("/contact",methods = ['GET','POST'])
@login_required
def contact():
    if(request.method ==  'POST'):

        '''add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        '''upload sno, name, email, phone num, message, date on database'''
        entry = Contact(name=name, email=email, phone_no=phone,message=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from blog ' + str(parameter['blog_name']) + ' by ' + name,
                             sender=email, recipients = [parameter['gmail_id']],
                             body = message +"\n"+phone)
    return render_template('contact.html',param=parameter)

@app.route("/post/<post_slug>", methods=['GET'] )
@login_required
def post_fetch(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',param=parameter,post=post)

@app.route("/register",methods = ['GET','POST'])
def register():
    return render_template('register.html',param=parameter)

@app.route("/userlogin",methods = ['GET','POST'])
def userlogin():
    return render_template('userlogin.html',param=parameter)

@app.route("/logout",methods = ['GET','POST'])
def logout():
    return render_template('logout.html',param=parameter)

@app.route("/dashboard",methods = ['GET','POST'])
def dashboard():
    posts = Posts.query.filter_by().all()[0:10]
    return render_template('dashboard.html',param=parameter,posts=posts)
app.run(debug = True)
