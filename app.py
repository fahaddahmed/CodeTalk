import os
from socket import socket
from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from passlib.hash import pbkdf2_sha256
from wtform_fields import *
from models import *

# Flask application configuration
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')  # Set the secret key for the application

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db.init_app(app)
engine_container = db.get_engine(app)

db = SQLAlchemy(app)  # Initialize SQLAlchemy with Flask app

socketio = SocketIO(app)  # Set up SocketIO with Flask app
CHATROOMS = ["courses", "coop", "resume", "stand-up", "other"]  # Predefined chatrooms

login = LoginManager(app)  # Configure the Flask-Login manager
login.init_app(app)

@login.user_loader  
def load_user(id):
    """ Load user by ID """
    return User.query.get(int(id))

# Routes for user authentication and interaction
@app.route("/", methods=['GET', 'POST'])
def index():
    """ Route for handling the login page """
    user_login_form = UserLoginForm()  # Instantiate login form
    
    if user_login_form.validate_on_submit():
        cur_user = User.query.filter_by(username=user_login_form.username.data).first()
        login_user(cur_user)
        return redirect(url_for('chat'))

    return render_template("login.html", form=user_login_form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """ Route for handling the registration page """
    user_reg_form = RegistrationForm()  # Instantiate registration form
    
    if user_reg_form.validate_on_submit():
        current_username = user_reg_form.username.data
        current_password = user_reg_form.password.data
        hash_password = pbkdf2_sha256.hash(current_password)  # Hash the password
        
        cur_user = User(username=current_username, password=hash_password)
        db.session.add(cur_user)
        db.session.commit()  # Commit the new user to the database

        flash('Registered Successfully')
        return redirect(url_for('index'))

    return render_template("index.html", form=user_reg_form)

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    """ Route for the chat page, checks for authenticated user """
    if not current_user.is_authenticated:
        flash('Must be logged in before accessing chat')
        return redirect(url_for('index'))

    user_room_add = AddRoomForm()  # Form for adding new chat r
