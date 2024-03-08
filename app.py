from flask import Flask, request, render_template, redirect, flash, jsonify, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User 

def create_app(db_name, testing=False):
    app = Flask(__name__)
    app.testing = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = "oh-so-secret"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    debug = DebugToolbarExtension(app)
    if app.testing:
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
    else:
        app.config['SQLALCHEMY_ECHO'] = True 

    @app.route('/')
    def redirect_to_users_list():
        return redirect("/users")

    @app.route('/users')
    def list_all_users():
        users = User.query.order_by(User.last_name, User.first_name).all()
        return render_template('users_list.html', users=users)

    @app.route('/users/new')
    def add_user_form():
        return render_template("add_user_form.html")

    @app.route('/users/new', methods=["POST"])
    def add_user():
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image_url"] if request.form["image_url"] else None

        if not first_name:
            flash("Please enter in a first name!")
            return redirect('/users/new')

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

    @app.route('/users/<int:user_id>/edit', methods=["POST"])
    def update_user(user_id):
        updated_user = User.query.get_or_404(user_id)

        if not request.form["first_name"]:
            flash("The user's first name cannot be empty!")
            return redirect(f'/users/{user_id}/edit')

        updated_user.first_name = request.form["first_name"]
        updated_user.last_name = request.form["last_name"]
        updated_user.image_url = request.form["image_url"]

        db.session.add(updated_user)
        db.session.commit()

        return redirect('/users')

    @app.route('/users/<int:user_id>/delete', methods=["POST"])
    def delete_user(user_id):
        User.query.filter_by(id=user_id).delete()

        db.session.commit()

        return redirect('/users')

    return app

if __name__ == '__main__':
    app = create_app('bloggit')
    connect_db(app)
    app.run(debug=True)


# app.app_context().push()
