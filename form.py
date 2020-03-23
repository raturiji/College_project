from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired(),Length(max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(max=25)])
    email = StringField('Email',validators=[DataRequired(),Email(),Length(max=50)])
    phone_number = StringField('Contact No.',validators=[DataRequired(),Length(10)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
    confirm_password = PasswordField('Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up',)


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email(),Length(max=50)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
    submit = SubmitField('Login')
