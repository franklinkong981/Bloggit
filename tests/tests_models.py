"""This file contains some tests for the methods and class methods found inside the Model classes."""
from unittest import TestCase
from app import create_app
from models import db, connect_db, User

# Create another application instance that connects to the testing database (bloggit_test) instead fo the main database (bloggit).
app = create_app("bloggit_test", testing=True)
connect_db(app)
app.app_context().push()

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_get_full_name(self):
        user = User(first_name="TestUser", last_name="Zach")
        self.assertEqual(user.get_full_name(), "TestUser Zach")
