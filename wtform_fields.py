from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import User


def valid_user_data(form, field):
    """Verifies user credentials during the login process."""
    current_username = form.username.data
    current_password = field.data

    # Check if user exists and password is correct
    user_query = User.query.filter_by(username=current_username).first()
    if user_query is None or not pbkdf2_sha256.verify(current_password, user_query.password):
        raise ValidationError("Invalid login details provided.")


def validate_registration(form, field):
    """Checks if a username is already taken during registration."""
    username_attempt = field.data

    # Query database for existing user
    existing_user = User.query.filter_by(username=username_attempt).first()
    if existing_user:
        raise ValidationError("This username is already in use. Please choose a different one.")


class RegistrationForm(FlaskForm):
    """Form for new user registration."""
    username = StringField('Username', validators=[
        InputRequired(message="Username is required."),
        Length(min=4, max=25, message="Username length must be between 4 and 25 characters."),
        validate_registration
    ])

    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required."),
        Length(min=5, message="Password length must be more than 4 characters.")
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(message="Confirmation of password is required."),
        EqualTo('password', message="Both passwords must match.")
    ])

    submit_button = SubmitField('Register')


class UserLoginForm(FlaskForm):
    """Form for existing user login."""
    username = StringField('Username', validators=[InputRequired(message="Username is required.")])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required."), valid_user_data
    ])
    submit_button = SubmitField('Sign In')


class AddRoomForm(FlaskForm):
    """Form to add a new room."""
    roomname = StringField('Room Name', validators=[
        InputRequired(message="Please enter a room name."),
        Length(min=2, max=15, message="Room name must be between 2 and 15 characters.")
    ])

    submit_button = SubmitField('Add Room')

