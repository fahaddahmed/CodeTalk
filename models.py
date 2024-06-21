from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize SQLAlchemy to work with Flask
db = SQLAlchemy()

class User(UserMixin, db.Model):
    # Specifies the name of the table in the database
    __tablename__ = "user_table"

    # Define columns for the table
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    username = db.Column(db.String(25), unique=True, nullable=False)  # User's username, must be unique and provided
    password = db.Column(db.String(), nullable=False)  # User's password, cannot be empty

    # Constructor for creating a new User object
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Representation method to display information about the object
    def __repr__(self):
        return f"<User {self.username}>"
