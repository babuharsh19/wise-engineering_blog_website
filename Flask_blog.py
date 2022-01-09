from flask import Flask, render_template, request,url_for,Blueprint,flash,redirect
from allmodels import Contacts,Post,Users,Admin,app,db
import pymysql
import json
import datetime
from flask_mail import Mail
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import math
import requests
from werkzeug.utils import secure_filename

core = Blueprint('core',__name__)

with open('config.json','r') as f:
    parameter = json.load(f)["parameters"]

local_server = True
app.config['UPLOAD_FOLDER'] = parameter['upload_location']
app.config.update(
    MAIL_SERVER ='smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = parameter['gmail_id'],                                                                       
    MAIL_PASSWORD = parameter['gmail_password']
)
mail = Mail(app)


@app.route("/home")
@login_required
def home():
    posts = Post.query.filter_by().all()
    last = math.ceil(len(posts)/3)
    page=request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*3:((page-1)*3+ 3)]
    if page==1:
        prev = "#"
        if page==last:
            next = "#"
        else:
            next = "/?page="+ str(page+1)
    elif page==last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)
    return render_template("index.html",param=parameter,posts=posts,prev=prev,next=next)

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
        entry = Contacts(name=name, email=email, phone_no=phone,message=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from blog ' + str(parameter['blog_name']) + ' by ' + name,
                             sender=email, recipients = [parameter['gmail_id']],
                             body = message +"\n"+phone)
    return render_template('contact.html',param=parameter)

@app.route("/post/<post_slug>", methods=['GET'] )
@login_required
def post_fetch(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    return render_template('post.html',param=parameter,post=post)

@app.route('/news',methods=['GET', 'POST'])
@login_required
def technews():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=2e30219277054eeab3f13200b9ac3cb1"
    r = requests.get(url).json()
    cases = {
        'articles' : r['articles']
    }
    return render_template('tech-news.html',case=cases,param=parameter)

@app.route("/register",methods = ['GET','POST'])
def registeration():
    if(request.method ==  'POST'):

        '''add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('psw')
        user = Users.query.filter_by(email= email).first()
        if user:
            flash('Sorry, This email is already registered!')
            return redirect(url_for('registration'))
        else:
            entry = Users(name=name,email=email,password=generate_password_hash(password, method='sha256'))
            db.session.add(entry)
            db.session.commit()
            redirect(url_for('login.html'))
    return render_template('register.html',param=parameter)

@app.route("/userlogin",methods = ['GET','POST'])
def userlogin():
    if request.method == ['GET','POST']:
        email = request.form.get('email')
        password = request.form.get('psw')
        remember = True if request.form.get('remember') else False
        user = Users.query.filter_by(email= email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Either you are not registered or your password is incorrect")
            return redirect(url_for('userlogin'))
        else:
            login_user(user, remember=remember)
            flash("Loggedin succesfully")
            return redirect(url_for('home'))
    return render_template('userlogin.html',param=parameter)

@app.route("/adminlogin",methods = ['GET','POST'])
def adminlogin():
    if request.method == ['GET','POST']:
        email = request.form.get('email')
        password = request.form.get('password')
        admin = Admin.query.filter_by(email= email).first()
        if admin.password == password and admin is not None:
            flash("Loggedin succesfully")
            login_user(admin)
            posts = Post.query.filter_by().all()[0:3]
            return render_template("admin-login.html",param=parameter,posts=posts)
        else:
            flash("Either you are not Admin or your password is incorrect")
    return render_template('adminlogin.html',param=parameter)

@app.route("/edit/<sno>", methods=['GET','POST'] )
@login_required
def edit_post(sno):
    email=Admin.query.get('email')
    if(request.method ==  'POST' and current_user.email==email):
      title = request.form.get('title')
      subheading = request.form.get('subheading')
      slug = request.form.get('slug')
      content = request.form.get('content')
      img_file = request.form.get('img_file')
      date=datetime.now()  
      post = Post.query.filter_by(sno=sno).first()
      post.title=title
      post.subheading=subheading
      post.slug=slug
      post.content=content
      post.img_file=img_file
      post.date=date
      db.session.commit()
      return redirect(url_for('admin-panel.html'))
    post = Post.query.filter_by(sno=sno).first()  
    return render_template('edit.html',param=parameter,post=post,sno=sno)

@app.route("/add", methods=['GET','POST'] )
@login_required
def add_post():
    if(request.method ==  'POST'):
      title = request.form.get('title')
      subheading = request.form.get('subheading')
      slug = request.form.get('slug')
      content = request.form.get('content')
      img_file = request.form.get('img_file')
      date=datetime.now()  
      entry = Post(title=title,subheading=subheading,slug=slug,content=content,img_file=img_file,date=date)
      db.session.add(entry)
      db.session.commit()
      return redirect(url_for('/home'))  
    return render_template('add.html',param=parameter)

@app.route("/uploader" , methods=['GET', 'POST'])
@login_required
def uploader():
        if request.method=='POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded successfully!"

@app.route("/admin-panel")
@login_required
def admin_panel():
    email=Admin.query.get('email')
    if current_user.email==email:
        posts = Post.query.filter_by().all()
        return render_template('admin-panel.html',param=parameter,posts=posts)

@app.route("/delete/<sno>" , methods=['GET', 'POST'])
@login_required
def delete(sno):
    if current_user.email==Admin.query.get('email'):
        post = Post.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('/home'))


@app.route("/logout",methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


@app.route("/dashboard",methods = ['GET','POST'])
def dashboard():
    posts = Post.query.filter_by().all()[0:10]
    return render_template('dashboard.html',param=parameter,posts=posts)

app.run(debug = True)
