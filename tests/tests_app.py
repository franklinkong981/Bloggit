"""This file contains unit tests and integration tests for the main SQLAlchemy Flask app in a testing databse called bloggit_test."""
from unittest import TestCase
from app import create_app
from models import db, connect_db, User

# Create another application instance that connects to the testing database (bloggit_test) instead fo the main database (bloggit).
app = create_app("bloggit_test", testing=True)
connect_db(app)
app.app_context().push()

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Contains tests concerning the User model integrated with the main SQLAlchemy Flask app."""
    def setUp(self):
        """Delete current entries, and add 3 predefined Users as entries in the users table for testing."""
        User.query.delete()

        lucky = User(first_name="Lucky", last_name="Prescott")
        pru = User(first_name="Pru", last_name="Granger")
        abigail = User(first_name="Abigail", last_name="Stone")
        db.session.add(lucky)
        db.session.add(pru)
        db.session.add(abigail)

        db.session.commit()

        self.lucky_id = lucky.id
        self.pru_id = pru.id
        self.abigail_id = abigail.id

    def tearDown(self):
        """Cleans up tests and empties the staging area for the database."""
        db.session.rollback()


    def test_list_users(self):
        """Ensures sending a GET request to the form page redirects the user to the main /users page where each user in the database is listed."""
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users List', html)
            self.assertIn('Lucky', html)
            self.assertIn('Pru', html)
            self.assertIn('Abigail', html)

    def test_add_user(self):
        """Ensures adding a user which satisfies the required fields redirects the user to the users list page where the new user is included."""
        with app.test_client() as client:
            resp = client.post("/users/new", data={'first_name': 'John', 'last_name': 'Smith', 'image_url': ''}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Smith', html)


    def test_add_invalid_user(self):
        """Ensures that entering an empty first_name field to add a new user is detected and the user is redirected to the Add User form."""
        with app.test_client() as client:
            resp = client.post("/users/new", data={'first_name': '', 'last_name': 'Smith', 'image_url': ''})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/new")
    
    def test_user_details(self):
        """Ensures that sending a GET request to a valid existing user's details page takes us to the appropriate user details page."""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.lucky_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Details on User Lucky Prescott', html)
            self.assertIn('Edit User', html)
            self.assertIn('Delete User', html)
    
    def test_edit_user(self):
        """Ensures that updating a particular valid user's information, with all fields being valid, redirects us back to the list users
        page where the updated user's new full name is shown."""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.lucky_id}/edit", data={'first_name': 'Fortuna', 'last_name': 'Prescott', 'image_url': ''}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fortuna Prescott', html)
    
    def test_edit_invalid_user(self):
        """Ensures that updating a particular valid user's information with an empty first name field redirects back to that user's
        particular Edit User form."""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.lucky_id}/edit", data={'first_name': '', 'last_name': 'Prescott', 'image_url': ''})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"/users/{self.lucky_id}/edit")
    
    def delete_user(self):
        """Ensures that deleting a user removes them from the database, then redirects us back to the home page where the new user
        is no longer listed."""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.lucky_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Lucky Prescott', html)
