import unittest
import sys
import os
from datetime import date, timedelta
from app import app
from database import db, User, Task
from werkzeug.security import generate_password_hash

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestMangementTestCase(unittest.TestCase):

    """Set up test client and initialize test database before each test"""
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False # CSRF disabled for testing
        app.config['SECRET_KEY'] = 'test-key'

        self.app = app
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up database after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test 1: User Registrtion with valid inputs
    def test_user_registration_valid(self):
        """Test user registration with valid username, email, password"""
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password1234'
        }, follow_redirects=False)

        # Should redirect to login page after successful registration
        self.assertEqual(response.status_code, 302)

        # Verify user was  created in database
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'test@example.com')


    # Test 2: User Registrtion with invalid inputs(diplicate name)
    def test_user_registration_duplicate_name(self):
        """Test user registration failure when username already exists"""
        # Create user in database
        with app.app_context():
            user = User(
                username='existinguser',
                email='existing@example.com',
                password=generate_password_hash('Password123')
            )

        # Try to register user with same username
        response = self.client.post('/register', data={
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password': 'Password1234'
        }, follow_redirects=True)

        # Should show error message
        self.assertIn('Username already exists', response.data)

        
        
        


