from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember = BooleanField('remember me')
    loginbtn = SubmitField('Login')

class SignupForm(Form):
    firstname = StringField('firstname', validators=[DataRequired()],render_kw={"placeholder": "First Name"})
    lastname = StringField('lastname', validators=[DataRequired()],render_kw={"placeholder": "Last Name"})
    username = StringField('username', validators=[DataRequired()],render_kw={"placeholder": "username"})
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', [
    validators.DataRequired(),
    validators.EqualTo('confirmPassword', message='Passwords must match')],
    render_kw={"placeholder": "Password"})
    confirmPassword = PasswordField('ConfirmPassword', validators=[DataRequired()],render_kw={"placeholder": "Confirm Password"})
    consent = BooleanField('I consent site to store your email and password securely', validators=[DataRequired()])
    Signupbtn = SubmitField('Signup')

class PostForm(Form):
    title = StringField('title', validators=[DataRequired()],render_kw={"placeholder": "Title"})
    message = StringField('message', validators=[DataRequired()],render_kw={"placeholder": "message"})
    submitpost = SubmitField('Post')
