from flask_sqlalchemy import SQLAlchemy

# Initializing SQLAlchemy object
db = SQLAlchemy()

# Defining the User model/table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy='dynamic')

    def __repr__(self):
        return f'User {self.name}'


# Defining the Task model/table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}, User ID: {self.user_id}>'