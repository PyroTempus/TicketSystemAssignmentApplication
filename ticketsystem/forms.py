from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from ticketsystem.models import User, Ticket


# Form for registering to the website
class RegisterForm(FlaskForm):

    # Checks if a user exists with the same username and displays a flash message to the user if it does
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')

    def validate_email_address(self, email_to_check):
        email = User.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError(
                'Email address is already registered on this website. Please try another email address.')

    # The forms to put in information required to make an account
    username = StringField(label='Username', validators=[Length(min=4, max=20), DataRequired()])
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Register')


# Form to handle logging into the website
class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


# Form for creating new tickets /create route
class TicketCreationForm(FlaskForm):
    name = StringField(label='Title', validators=[DataRequired()])
    description = StringField(label='Description', validators=[Length(min=5, max=1024), DataRequired()])
    submit = SubmitField(label='Create Ticket')


# Form for updating tickets
class UpdateTicketForm(FlaskForm):
    name = StringField(label='Title', validators=[DataRequired()])
    description = StringField(label='Description', validators=[Length(min=5, max=1024), DataRequired()])
    submit = SubmitField(label='Update Ticket')
