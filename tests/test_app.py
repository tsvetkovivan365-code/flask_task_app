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
        self.assertIn(b'Username already exists', response.data)

    # Test 3: User Login - Successful attempt
    def test_user_login_success(self):
        """Test successful user login with correct credentials"""

        # Create user in database
        with app.app_context():
            user = User(
                username='testloginuser',
                email='testlogin@example.com',
                password=generate_password_hash('Password123')
            )
            db.session.add(user)
            db.session.commit()

        # Attempt login
        response = self.client.post('/login', data={
            'username': 'testloginuser',
            'password': 'Password123'
        }, follow_redirects=False)

        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)

    # Test 4: User Login - Failed attempt(wrong password)
    def test_user_login_failed(self):
        """Test failed user login with incorrect password"""

        # Create user in database
        with app.app_context():
            user = User(
                username='testloginuser',
                email='testlogin@example.com',
                password=generate_password_hash('Password123')
            )
            db.session.add(user)
            db.session.commit()

        # Attempt login with wrong password
        response = self.client.post('/login', data={
            'username': 'testloginuser',
            'password': 'password'
        }, follow_redirects=True)

        # Should show error message
        self.assertIn(b'Invalid username or password', response.data)

    # Test 5: Task Creation
    def test_task_creation(self):
        """Test creating a new task for authenticated user"""

        # Create logged in user
        with app.app_context():
            user = User(
                username='taskuser',
                email='task@example.com',
                password=generate_password_hash('Password123')
            )

            db.session.add(user)
            db.session.commit()
            user_id = user.id
        
        # Login
        self.client.post('/login', data={
            'username': 'taskuser',
            'password': 'Password123'
        })

        # Create task
        response = self.client.post('/create_task', data={
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': str(date.today() + timedelta(days=7)),
            'status': 'To Do',
            'priority': 'High'
        }, follow_redirects=False)

        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)

        # Verify task was created
        with app.app_context():
            task = Task.query.filter_by(user_id=user_id).first()
            self.assertIsNotNone(task)
            self.assertEqual(task.title, 'Test task')
            self.assertEqual(task.priority, 'High')

    # Test 6: Task Update
    def test_task_update(self):
        """Test updating an existing task"""
        # Create user and task
        with app.app_context():
            user = User(
                username='updateuser',
                email='update@example.com',
                password=generate_password_hash('Password123')
            )
            db.session.add(user)
            db.session.commit()

            task = Task(
                title='Original Title',
                description='Original Description',
                due_date=date.today() + timedelta(days=7),
                status='To Do',
                priority='Low',
                user_id=user.id
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        # Login
        self.client.post('/login', data={
            'username': 'updateuser',
            'password': 'Password123'
        })

        # Update task
        response = self.client.post(f'/tasks/{task_id}/edit', data={
            'title': 'Updated Title',
            'description': 'Updated Description',
            'due_date': str(date.today() + timedelta(days=14)),
            'status': 'In Progress',
            'priority': 'High'
        }, follow_redirects=False)

        # Verify task was updated
        with app.app_context():
            updated_task = Task.query.get(task_id)
            self.assertEqual(updated_task.title, 'Updated Title')
            self.assertEqual(updated_task.status, 'In Progress')
            self.assertEqual(updated_task.priority, 'High')

    # Test 7: Task Deletion
    def test_task_deletion(self):
        """Test deleting a task via API endpoint"""
        # Create user and task
        with app.app_context():
            user = User(
                username='deleteuser',
                email='delete@example.com',
                password=generate_password_hash('Password123')
            )
            db.session.add(user)
            db.session.commit()

            task = Task(
                title='Task to Delete',
                description='This task will be deleted',
                due_date=date.today() + timedelta(days=7),
                status='To Do',
                priority='Low',
                user_id=user.id
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        # Login
        self.client.post('/login', data={
            'username': 'deleteuser',
            'password': 'Password123'
        })

        # Delete a task
        response = self.client.delete(f'/api/tasks/{task_id}/delete')

        # Should return success
        self.assertEqual(response.status_code, 200)

        # Verify task has been deleted
        with app.app_context:
            deleted_task = Task.query.get(task_id)
            self.assertIsNone(deleted_task)
        
        
        


