"""This file contains the models for the Bloggit app, establishing the tables and columsn in tables in the bloggit database.
Models include Users and Posts."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

class User(db.Model):
    """User model. Each user will have an id (primary key), first name, last name, and an image URL for their profile picture.
    First name is required, but last name is not. Profile picture's url is also optional, users without one will have a default one."""
    
    __tablename__ = "users"

    def __repr__(self):
        return f"<User id={self.id} name={self.first_name} {self.last_name}>"
    
    def get_full_name(self):
        """Returns the full name (first name then last name) of a particular user. This method is here for convenience."""
        return f"{self.first_name} {self.last_name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=True, default="")
    image_url = db.Column(db.Text, nullable=True, default="https://cdn3.iconfinder.com/data/icons/letters-and-numbers-1/32/letter_B_red-512.png")
    
    posts = db.relationship('Post', cascade='all, delete', backref='author')

class Post(db.Model):
    """Post model. Each post that's created will have an id, title (which can be no longer than 50 characters), content text, 
    a date+time it was created at, and a user_id as a foreign key, which = the id of the user who authored the post."""
    
    __tablename__ = "posts"

    def __repr__(self):
        return f"<Post id={self.id} title={self.title} Created At: {self.created_at}> by {self.author.first_name} {self.author.last_name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



