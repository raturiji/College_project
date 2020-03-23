from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,ValidationError
from wtforms.validators import DataRequired,Length,Email,EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired(),Length(max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(max=25)])
    email = StringField('Email',validators=[DataRequired(),Email(),Length(max=50)])
    phone_number = StringField('Contact No.',validators=[DataRequired(),Length(10)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
    confirm_password = PasswordField('Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up',)

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email has already been taken. Please use another email')

    def validate_phone_number(self,phone_number):
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError('This phone number has already been taken. Please use another phone number')



class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email(),Length(max=50)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
    submit = SubmitField('Login')
