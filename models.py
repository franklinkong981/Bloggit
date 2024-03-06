from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model. Each user will have an id (primary key), first name, last name, and an image URL for their profile picture."""
    

