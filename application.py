from flask import Flask, render_template, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from time import localtime, strftime
import os

from wtform_fields import *
from models import *

from better_profanity import profanity

# configure app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET') # flask app secret key from heroku

# Initialize flask-SocketIO
socketio = SocketIO(app) 
# pre-defined rooms
ROOMS = ["lounge", "discussions", "news", "bakar", "coding"]

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') # sql database link from heroku
db = SQLAlchemy(app)

SQLALCHEMY_ENGINE_OPTIONS = {
    "max_overflow": 15,
    "pool_pre_ping": True,
    "pool_recycle": 60 * 60,
    "pool_size": 30,
}

# configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):

    return User.query.get(int(id))

# to remove sql-alchemy timeout error
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route("/", methods=['GET', 'POST'])
def index():

    # to avoid user to access signup page after being logged in
    if current_user.is_authenticated:
        return redirect(url_for('chat'))

    reg_form = RegistrationForm()

    # updated database if validation success
    if reg_form.validate_on_submit():

        # extract form data
        username = reg_form.username.data
        password = reg_form.password.data

        # generate hash using pbkdf2
        # we can also salt and number of iterations for password hashing using syntax: 
        # pbkdf2_sha256.using(rounds=1000, salt_size=8).hash(password)
        hashed_password = pbkdf2_sha256.hash(password)
        
        # add user to database
        user = User(username = username, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Regestired successfully. Please Login!!', category='success')

        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    # to avoid user to access login page after being logged in
    if current_user.is_authenticated:
        return redirect(url_for('chat'))

    login_form = LoginForm()

    # Allow login if validation is successful
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    # else return back to login page with validation errors
    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
# @login_required
def chat():

    if not current_user.is_authenticated:
        flash('Please login!', category='danger')
        return redirect(url_for('login'))

    return render_template("chat.html", username=current_user.username, rooms=ROOMS)

@app.route("/logout", methods=['GET'])
def logout():

    # to avoid user to access logout functationality without being logged in
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    logout_user()
    flash("You have logged out successfully!", category='success')
    return redirect(url_for('login'))

# defining event bucket for socketio
@socketio.on('message')
def message(data):
    # profanity filter
    print(data)
    profanity.load_censor_words()
    # print('msg ', profanity.censor(data['msg']), 'username ', data['username'], 'timestamp ', strftime('%d-%b %I:%M%p', localtime()), "room ", data['room'])
    send({'msg': profanity.censor(data['msg']), 'username': data['username'], 'timestamp': strftime('%d-%b %I:%M%p', localtime())}, room=data['room'])

@socketio.on('join')
def join(data):
    print("\n", data, "\n")
    join_room(data['room'])
    send({'msg': data['username']+" has joined the "+data['room']+" room!"}, room=data['room'])


@socketio.on('leave')
def leave(data):
    print("\n", data, "\n")
    leave_room(data['room'])
    send({'msg': data['username']+" has left the "+data['room']+" room!"}, room=data['room'])

if __name__ == "__main__":
    # socketio.run(app, debug=True)
    app.run() # using gunicorn server