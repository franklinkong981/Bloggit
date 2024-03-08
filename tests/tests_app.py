from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloggit_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

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
            resp = client.get("/")
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestPet', html)


    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.pet_id}")
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestPet</h1>', html)


    def test_add_invalid_user(self):
        with app.test_client() as client:
            d = {"name": "TestPet2", "species": "cat", "hunger": 20}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestPet2</h1>", html)
    
    def test_user_details(self):
        with app.test_client() as client:
            d = {"name": "TestPet2", "species": "cat", "hunger": 20}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestPet2</h1>", html)
    
    def test_edit_user(self):
        with app.test_client() as client:
            d = {"name": "TestPet2", "species": "cat", "hunger": 20}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestPet2</h1>", html)
    
    def test_edit_invalid_user(self):
        with app.test_client() as client:
            d = {"name": "TestPet2", "species": "cat", "hunger": 20}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestPet2</h1>", html)
    
    def delete_user(self):
        with app.test_client() as client:
            d = {"name": "TestPet2", "species": "cat", "hunger": 20}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestPet2</h1>", html)
