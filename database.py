from flask_sqlalchemy import SQLAlchemy
from flask_security.models import sqla

# Initializing SQLAlchemy object
db = SQLAlchemy()

# Setting up roles_users association table 
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

# Defining the User model/table
class User(db.Model, sqla.FsUserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(255))

    # Task relationship
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    # Role relationship via association table
    role = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.name}>'


# Defining the Task model/table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(12), default="To Do", nullable=False)
    due_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}, User ID: {self.user_id}>'
    
# Defining the Role model/table
class Role(db.Model, sqla.FsRoleMixin): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True)
    description = db.Column(db.Text)