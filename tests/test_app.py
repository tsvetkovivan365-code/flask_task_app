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
