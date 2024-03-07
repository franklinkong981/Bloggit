from flask import Flask, request, render_template, redirect, flash, jsonify, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User               

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloggit'
app.config['SQLALCHEMY_ECHO'] = 'true'
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

@app.route('/')
def redirect_to_users_list():
    return redirect("/users")

@app.route('/users')
def list_all_users():
    users = User.query.all()
    return render_template('users_list.html', users=users)

@app.route('/users/new')
def add_user_form():
    return render_template("add_user_form.html")