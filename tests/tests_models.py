from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloggit_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_get_full_name(self):
        user = User(first_name="TestUser", last_name="Zach")
        self.assertEquals(user.get_full_name(), "TestUser Zach")
