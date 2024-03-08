"""This file contains the models for the Bloggit app, establishing the tables and columsn in tables in the bloggit database.
Models include Users and Posts."""
from flask_sqlalchemy import SQLAlchemy

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

