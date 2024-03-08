# Seed file to make sample data for tables for Users and Posts so I can start off with some sample data on the first test.

from models import User, db, connect_db
from app import create_app

app = create_app('bloggit')
connect_db(app)
app.app_context().push()

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add starting users
franklin = User(first_name='Franklin', last_name='Kong', image_url='https://img.freepik.com/free-photo/ultra-detailed-nebula-abstract-wallpaper-4_1562-749.jpg')
jeffrey = User(first_name='Jeffrey', last_name='Kong', image_url='https://t4.ftcdn.net/jpg/01/25/86/35/360_F_125863509_jaISqQt7MOfhOT3UxRTHZoEbMmmFYIr8.jpg')
kenny = User(first_name='Kenny', last_name='Xu')

# Add and commit starting users to the database.
db.session.add(franklin)
db.session.add(jeffrey)
db.session.add(kenny)

db.session.commit()
