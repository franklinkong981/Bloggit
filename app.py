"""This file contains the method for creating an application instance and the routes for the main Bloggit application."""
from flask import Flask, request, render_template, redirect, flash, jsonify, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

def create_app(db_name, testing=False):
    """Create an instance of the app so I can have a production database and a separate testing database."""
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
    def show_homepage():
        """Home page. This will show the 5 most recent blog posts from any user and list the title, content, and date/time of 
        creation for each one."""
        recent_posts = Post.query.order_by(Post.id.desc()).limit(5)
        return render_template('home.html', posts=recent_posts)

    @app.route('/users')
    def list_all_users():
        """Lists all users by their full name (first name then last name) currently in the database."""
        users = User.query.order_by(User.last_name, User.first_name).all()
        return render_template('users_list.html', users=users)

    @app.route('/users/new')
    def add_user_form():
        """Displays a form to add a new user by typing in the user's first name, last name, and an optional image url for their profile picture."""
        return render_template("add_user_form.html")

    @app.route('/users/new', methods=["POST"])
    def add_user():
        """Adds a new user to the database and redirects to the main page where the new user is displayed.
        All fields are optional EXCEPT for first name field, user must provide a first name or they will be taken back
        to the add user form and an error message will be displayed."""
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image_url"] if request.form["image_url"] else None

        if not first_name:
            flash("Please enter in a first name!")
            return redirect('/users/new')

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        flash("User successfully added!")
        return redirect('/users')

    @app.route('/users/<int:user_id>')
    def show_user_details(user_id):
        """Shows detailed information about the user on their own page, including the user's profile picture and their full name, with
        buttons to edit the user information as well as delete the user from the database. Also shows a list of their posts as links
        to pages where users can see each post, and finally a button to add a new post."""
        user = User.query.get_or_404(user_id)
        posts = Post.query.filter_by(user_id=user_id).order_by(Post.id.desc()).all()
        return render_template("user_details.html", user=user, posts=posts)

    @app.route('/users/<int:user_id>/edit')
    def edit_user_form(user_id):
        """Displays a form to edit a user's informationthat looks like the add user form, but the fields are already pre-filled 
        with the user's information (first name, last name, and image url). Submitting the form will update this particular
        user's information."""
        user = User.query.get_or_404(user_id)
        return render_template("edit_user_form.html", user=user)

    @app.route('/users/<int:user_id>/edit', methods=["POST"])
    def update_user(user_id):
        """Submits the edit user form for a particular user. Once again, if the first name field is empty, you will be sent 
        back to the edit user form with an error message. Otherwise, redirects to /users page showing the user's new full name."""
        updated_user = User.query.get_or_404(user_id)

        if not request.form["first_name"]:
            flash("The user's first name cannot be empty!")
            return redirect(f'/users/{user_id}/edit')

        updated_user.first_name = request.form["first_name"]
        updated_user.last_name = request.form["last_name"]
        updated_user.image_url = request.form["image_url"]

        db.session.add(updated_user)
        db.session.commit()

        flash("User successfully updated!")
        return redirect('/users')

    @app.route('/users/<int:user_id>/delete', methods=["POST"])
    def delete_user(user_id):
        """Deletes the user with the specific user_id's information from the database, redirects you to the users list page."""
        user_to_delete = User.query.get_or_404(user_id)

        db.session.delete(user_to_delete)
        db.session.commit()

        flash("User successfully deleted!")
        return redirect('/users')
    
    @app.route('/users/<int:user_id>/posts/new')
    def add_post_form(user_id):
        """Displays the form for adding a new post for the user whose id is user_id. There are 2 fields in this form: Title and content.
        Both are required and the title can't be more than 50 characters."""
        user = User.query.get_or_404(user_id)
        return render_template("add_post_form.html", user=user)
    
    @app.route('/users/<int:user_id>/posts/new', methods=["POST"])
    def add_post(user_id):
        """Submits the add post form for a particular user. If the title/content fields are empty OR title field is more than 50 characters,
        redirects you back to the form with error messages. Otherwise, successfuly adds the post to the database and redirects to the user's
        details page."""
        user = User.query.get_or_404(user_id)
        error_count = 0

        title = request.form["title"]
        content = request.form["content"]
        # Check for errors
        if not title:
            flash("You must include a title!")
            error_count += 1
        elif len(title) > 50:
            flash("Your title can't be longer than 50 characters!")
            error_count += 1
        if not content:
            flash("You must include content in your post!")
            error_count += 1
        
        if error_count > 0:
            return redirect(f'/users/{user_id}/posts/new')
        
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        flash("Post successfully added!")
        return redirect(f'/users/{user_id}')
    
    @app.route('/posts/<int:post_id>')
    def show_post_details(post_id):
        """Show the details for the post with the id of post_id. Includes the title, content, author, and links to go to the 
        detailed author page, edit the post, and delete the post."""
        post = Post.query.get_or_404(post_id)
        tags = post.tags
        return render_template("post_details.html", post=post, tags=tags)
    
    @app.route('/posts/<int:post_id>/edit')
    def edit_post_form(post_id):
        """Display the form that allows the user to update a particular post with the title and content fields already prefilled
        with the title and content of the current version of the post."""
        post = Post.query.get_or_404(post_id)
        return render_template("edit_post_form.html", post=post)
    
    @app.route('/posts/<int:post_id>/edit', methods=["POST"])
    def update_post(post_id):
        """Submits the edit post form for a particular user. If the title/content fields are empty OR title field is more than 50 characters,
        redirects you back to the edit postform with error messages. Otherwise, successfuly updates the post in the database and redirects to the user's
        post view page."""
        post = Post.query.get_or_404(post_id)
        error_count = 0

        # Check for errors
        if not request.form["title"]:
            flash("You must include a title!")
            error_count += 1
        elif len(request.form["title"]) > 50:
            flash("Your title can't be longer than 50 characters!")
            error_count += 1
        if not request.form["content"]:
            flash("You must include content in your post!")
            error_count += 1
        
        if error_count > 0:
            return redirect(f'/posts/{post_id}/edit')
        
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.add(post)
        db.session.commit()
        flash("Post successfully updated!")
        return redirect(f'/posts/{post_id}')
    
    @app.route('/posts/<int:post_id>/delete', methods=["POST"])
    def delete_post(post_id):
        """Deletes the post with the specific post_id's information from the database, redirects you to the post's  author's list page."""
        post_to_delete = Post.query.get_or_404(post_id)
        author_id = post_to_delete.user_id

        db.session.delete(post_to_delete)
        db.session.commit()

        flash("Post successfully deleted!")
        return redirect(f'/users/{author_id}')
    
    @app.route('/tags')
    def show_tags():
        """Shows a list of all current tags. Each tag name is also a link to a more detailed page about that tag."""
        tags = Tag.query.all()
        return render_template('tags_list.html', tags=tags)
    
    @app.route('/tags/<int:tag_id>')
    def show_tag_details(tag_id):
        """Shows the list of posts associated with the specific tag."""
        current_tag = Tag.query.get_or_404(tag_id)
        posts = current_tag.posts
        return render_template('tag_details.html', tag=current_tag, posts=posts)
    
    @app.route('/tags/new')
    def add_tag_form():
        """Shows the form for adding a tag. Users can enter a name and submit to add the tag. Tag name must be unique and must be
        50 characters or less"""
        return render_template('add_tag_form.html')
    
    @app.route('/tags/new', methods=["POST"])
    def add_tag():
        """Processes the form data to add a new tag. If successful and all constraints are followed, redirects to the tags list page
        where the new added tag is now included. If not, redirects to the add tag form and displays error messages."""
        error_count = 0
        tag_name = request.form["tag_name"]

        #Check for errors
        if not tag_name:
            error_count += 1
            flash("The tag name can't be empty. Please enter a tag name.")
        elif len(tag_name) > 50:
            error_count += 1
            flash("The tag name can't be more than 50 characters.")
        all_tags = Tag.query.all()
        for tag in all_tags:
            if tag_name == tag.name:
                error_count += 1
                flash("The tag name must be unique! Please enter a tag name that doesn't already exist.")
                break;
        
        if error_count > 0:
            return redirect(f'/tags/new')
        new_tag = Tag(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()

        flash("Tag successfully added!")
        return redirect('/tags')
    
    @app.route('/tags/<int:tag_id>/edit')
    def edit_tag_form(tag_id):
        """Shows the form to edit/update the tag. The tag still has to be unique, and has to be between 1 and 50 characters."""
        tag_to_edit = Tag.query.get_or_404(tag_id)
        return render_template("edit_tag_form.html", tag=tag_to_edit)
    
    @app.route('/tags/<int:tag_id>/edit', methods=["POST"])
    def update_tag(tag_id):
        """Checks the updated tag from the edit tag form submission to see if it's still the proper length and unique. If it is, update
        the tag in the database and redirect to the tags list page. If not, redirect to edit tag form and display error messages."""
        tag_to_update = Tag.query.get_or_404(tag_id)
        error_count = 0
        tag_name = request.form["tag_name"]

        #Check for errors
        if not tag_name:
            error_count += 1
            flash("The tag name can't be empty. Please enter a tag name.")
        elif len(tag_name) > 50:
            error_count += 1
            flash("The tag name can't be more than 50 characters.")
        all_tags = Tag.query.all()
        for tag in all_tags:
            if tag.id != tag_id and tag_name == tag.name:
                error_count += 1
                flash("The tag name must be unique! Please enter a tag name that doesn't already exist.")
                break
        
        if error_count > 0:
            return redirect(f'/tags/{tag_id}/edit')
        tag_to_update.name = tag_name
        db.session.add(tag_to_update)
        db.session.commit()

        flash("Tag successfully updated!")
        return redirect('/tags')
    
    @app.route('/tags/<int:tag_id>/delete', methods=["POST"])
    def delete_tag(tag_id):
        """Deletes the tag and deletes any associations between this tag and all posts."""
        tag_to_delete = Tag.query.get_or_404(tag_id)
        db.session.delete(tag_to_delete)
        db.session.commit()

        flash("Tag successfully deleted!")
        return redirect('/tags')

    @app.errorhandler(404) 
    def not_found(e): 
        return render_template("404.html") 

    return app

if __name__ == '__main__':
    app = create_app('bloggit')
    connect_db(app)
    app.run(debug=True)


# app.app_context().push()
