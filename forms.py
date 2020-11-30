from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, NumberRange
import email_validator


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=6, max=55)])
    email = StringField("Email", validators=[
                        InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[
                            InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=6, max=55)])


class FeedbackForm(FlaskForm):
    """Form for adding/updating feedback"""

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[
                          InputRequired(), Length(max=100)])


class DeleteForm(FlaskForm):
    """Intentionally Empty"""
