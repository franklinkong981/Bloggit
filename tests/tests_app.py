from unittest import TestCase
from app import create_app
from models import db, connect_db, User

app = create_app("bloggit_test", testing=True)
connect_db(app)
app.app_context().push()

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    def setUp(self):
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
        db.session.rollback()


    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users List', html)
            self.assertIn('Lucky', html)
            self.assertIn('Pru', html)
            self.assertIn('Abigail', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.post("/users/new", data={'first_name': 'John', 'last_name': 'Smith', 'image_url': ''}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Smith', html)


    def test_add_invalid_user(self):
        with app.test_client() as client:
            resp = client.post("/users/new", data={'first_name': '', 'last_name': 'Smith', 'image_url': ''})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/new")
    
    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.lucky_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Details on User Lucky Prescott', html)
            self.assertIn('Edit User', html)
            self.assertIn('Delete User', html)
    
    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.lucky_id}/edit", data={'first_name': 'Fortuna', 'last_name': 'Prescott', 'image_url': ''}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fortuna Prescott', html)
    
    def test_edit_invalid_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.lucky_id}/edit", data={'first_name': '', 'last_name': 'Prescott', 'image_url': ''})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"/users/{self.lucky_id}/edit")
    
    def delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.lucky_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Lucky Prescott', html)
