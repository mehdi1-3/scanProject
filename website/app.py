from asyncio.windows_events import NULL
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_login import UserMixin
from sqlalchemy.sql import func

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
#from website.models import Note
#from . import db
import json

from flask import Blueprint, render_template, request, flash, redirect, url_for
#from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
#from .. import db
from flask_login import login_user, login_required, logout_user, current_user

from asyncio.windows_events import NULL
from flask import Flask, render_template, url_for, request,Response,json, Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path
import website.models as models
import osdetect, checkport,hostdetection

db = SQLAlchemy()
DB_NAME = "database.db"

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) > 15:
            flash('This IP address is NOT valid! ', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('IP address added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

#///////////////////////////////////////////////////////////////////////
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

#////////////////////////////////////////////////////////////////////

cyberz = Blueprint('cyberz', __name__)

# @cyberz.route('/')
# def index():
#     return render_template("index.html")

@cyberz.route('/port-scan',methods=['GET','POST'])
@login_required
def portScan():
    if request.method=='POST':
        domain=request.form.get('domain')
        minrange=int(request.form.get('minrange'))
        maxrange=int(request.form.get('maxrange'))
        L=checkport.check_range(domain,minrange,maxrange)
        
        L=(json.dumps(L)).split(",")
        L_index=[x for x in range (1,len(L)+1)]
        zipped=zip(L,L_index)
        return render_template("scanport.html",zipped=zipped)

    return render_template("scanport.html", user=current_user)




@cyberz.route('/os-informations', methods=['GET','POST'])
@login_required
def osInfo():
    if request.method=='POST':
        domain=request.form.get('domain')
        resp=osdetect.osdetection(domain)
        print(len(resp))
        if len(resp) == 9:
            return (render_template("os_info.html",msg="This IP address is unknown, Check port scan or firewall detection for further informations"))
        else:
            resp=resp.replace(":",",").split(",")
            list1=[resp[0][1:],resp[2][1:],resp[4][1:],resp[6][1:],resp[8][1:]]
            #print (list1)
            list2=[resp[1],resp[3],resp[5],resp[7],resp[9][:len(resp[9])-1]]
            zipped=zip(list1,list2)
            return render_template("os_info.html",zipped=zipped, user=current_user)
            #return osdetect.osdetection(domain)

    return render_template("os_info.html", user=current_user)




@cyberz.route('/host-detection', methods=['GET','POST']) 
@login_required
def host():
    if request.method=='POST':    
        domain=request.form.get('domain')
        resp=json.dumps({'active hosts': hostdetection.activeHosts(domain)}).split(",")
        index=[x for x in range(1,len(resp))]
        zipped=zip(resp[1:],index)
        return render_template("host.html",zipped=zipped, user=current_user)
    
    return render_template("host.html", user=current_user)

#//////////////////////////////////////////////////


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #from .views import views
    #from .auth import auth
    #from .cyberz import cyberz

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(cyberz, url_prefix='/')

    #from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
        if not path.exists('website/' + DB_NAME):
            db.create_all(app=app)
            print('Created Database!')



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(15))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
