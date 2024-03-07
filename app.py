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

@app.route('/users/new', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] if request.form["image_url"] else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", user=user)

@app.route('/users/<int:user_id>/edit')
def update_user(user_id):
    updated_user = User.query.get_or_404(user_id)

    updated_user.first_name = request.form["first_name"]
    updated_user.last_name = request.form["last_name"]
    updated_user.image_url = request.form["image_url"]

    db.session.add(updated_user)
    db.session.commit()

    return redirect('/users')

