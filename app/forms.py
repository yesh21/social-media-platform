from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    loginbtn = SubmitField('Login')

class SignupForm(Form):
    username = PasswordField('username', validators=[DataRequired()],render_kw={"placeholder": "username"})
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    confirmPassword = PasswordField('ConfirmPassword', validators=[DataRequired()],render_kw={"placeholder": "Confirm Password"})
    consent = BooleanField('I consent site to store your email and password securely', validators=[DataRequired()])
    Signupbtn = SubmitField('Signup')