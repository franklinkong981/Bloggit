# Seed file to make sample data for tables for Users and Posts so I can start off with some sample data on the first test.

from models import User, Post, Tag, PostTag, db, connect_db
from app import create_app

app = create_app('bloggit')
connect_db(app)
app.app_context().push()

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# Create starting users
franklin = User(first_name='Franklin', last_name='Kong', image_url='https://img.freepik.com/free-photo/ultra-detailed-nebula-abstract-wallpaper-4_1562-749.jpg')
jeffrey = User(first_name='Jeffrey', last_name='Kong', image_url='https://t4.ftcdn.net/jpg/01/25/86/35/360_F_125863509_jaISqQt7MOfhOT3UxRTHZoEbMmmFYIr8.jpg')
kenny = User(first_name='Kenny', last_name='Xu')

# Create starting posts
franklin_post1 = Post(title="My First Post", content="Hi Everyone! Welcome to my Blog! Nice to meet you!", user_id=1)
franklin_post2 = Post(title="My Springboard Progress", content="I am currently working on the Blogly project in Springboard!", user_id=1)
jeffrey_post1 = Post(title="Good Morning!", content="""I really enjoyed the weather this morning! There was a nice blue sky and I 
                     got to enjoy the morning doves chirping as well!""", user_id=2)
jeffrey_post2 = Post(title="Thoughts on Springboard", content="I think the bootcamp my brother is doing is really wonderful!", user_id=2)
kenny_post1 = Post(title="Welcome to my Startup Blog!", content="""Hi friends! Welcome to my blog where I'll post continual
                   developments over my recent startup! It's going to be lots of fun!""", user_id=3)

# Create starting tags
tag1 = Tag(name='Weather')
tag2 = Tag(name='Startup')
tag3 = Tag(name='First Post')
tag4 = Tag(name='Springboard')

# Create starting post tags:
post_tag1 = PostTag(post_id=1, tag_id=3)
post_tag2 = PostTag(post_id=2, tag_id=4)
post_tag3 = PostTag(post_id=3, tag_id=3)
post_tag4 = PostTag(post_id=3, tag_id=1)
post_tag5 = PostTag(post_id=4, tag_id=4)
post_tag6 = PostTag(post_id=5, tag_id=3)
post_tag7 = PostTag(post_id=5, tag_id=2)

# Add and commit starting users and posts to the database.
db.session.add_all([franklin, jeffrey, kenny])
db.session.commit()
db.session.add_all([tag1, tag2, tag3, tag4])
db.session.commit()
db.session.add_all([franklin_post1, franklin_post2, jeffrey_post1, jeffrey_post2, kenny_post1])
db.session.commit()
db.session.add_all([post_tag1, post_tag2, post_tag3, post_tag4, post_tag5, post_tag6, post_tag7])
db.session.commit()
