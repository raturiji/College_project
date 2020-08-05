from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,ValidationError,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from app.models import User,Property

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired(),Length(max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(max=25)])
    email = StringField('Email',validators=[DataRequired(),Email(),Length(max=50)])
    phone_number = StringField('Contact No.',validators=[DataRequired(),Length(10)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
    confirm_password = PasswordField('Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

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

class PostAddForm(FlaskForm):
    postTypeChoices = [('Select','Select'),('1 BHK','1 BHK'),('2 BHK','2 BHK'),('3 BHK','3 BHK'),('4 BHK','4 BHK')]
    stateChoices = [('Select','Select'),('Andhra Pradesh','Andhra Pradesh'),('Arunachal Pradesh','Andhra Pradesh'),('Assam','Assam'),('Bihar','Bihar'),('Chhattisgarh','Chhattisgarh'),('Goa','Goa'),('Gujarat','Gujarat'),('Haryana','Haryana'),
                    ('Himachal Pradesh','Himachal Pradesh'),('Jammu And Kashmir','Jammu And Kashmir'),('Jharkhand','Jharkhand'),('Karnatka','Karnatka'),('Kerala','Kerala'),('Madhya Pradesh','Madhya Pradesh'),('Maharashtra','Maharashtra'),
                    ('Manipur','Manipur'),('Meghalaya','Meghalaya'),('Mizoram','Mizoram'),('Nagaland','Nagaland'),('Odisha','Odisha'),('Punjab','Punjab'),('Rajasthan','Rajasthan'),('Sikkim','Sikkim'),('Tamil Nadu','Tamil Nadu'),
                    ('Telangana','Telangana'),('Tripura','Tripura'),('Uttar Pradesh','Uttar Pradesh'),('Uttarakhand','Uttarakhand'),('West Bengal','West Bengal')]
    tenantChoices = [('Select','Select'),('Family','Family'),('Bachelor','Bachelor')]
    property_type = SelectField(u'Property Type', choices = postTypeChoices, validators = [DataRequired()])
    state = SelectField(u'State', choices = stateChoices, validators = [DataRequired()])
    city = StringField('Price',validators=[DataRequired()])
    tenant = SelectField(u'Tenant', choices = tenantChoices, validators = [DataRequired()])
    address = TextAreaField('Address',validators = [DataRequired(),Length(max=100)] )
    description = TextAreaField('Description',validators = [DataRequired(),Length(max=200)] )
    price = StringField('Price',validators=[DataRequired()])
    submit = SubmitField('Submit') 

    def validate_property_type(self,property_type):
        if property_type.data == 'Select':
            raise ValidationError(' Property Type detail is required. Please select a propety type ')

    def validate_state(self,state):
        if state.data == 'Select':
            raise ValidationError(' State detail is required. Please select a State ')

    def validate_tenant(self,tenant):
        if tenant.data == 'Select':
            raise ValidationError(' Tenant detail is required. Please select a Tenant ')

    def validate_address(self,address):
        address = Property.query.filter_by(address=address.data).first()
        if address:
            raise ValidationError('This address has already been taken. Please use another address')
    
    def validate_description(self,description):
        description = Property.query.filter_by(description=description.data).first()
        if description:
            raise ValidationError('This description has already been taken. Please use another description')

class SearchForm(FlaskForm):
    postTypeChoices = [('Select','Select'),('1 BHK','1 BHK'),('2 BHK','2 BHK'),('3 BHK','3 BHK'),('4 BHK','4 BHK')]
    stateChoices = [('Select','Select'),('Andhra Pradesh','Andhra Pradesh'),('Arunachal Pradesh','Andhra Pradesh'),('Assam','Assam'),('Bihar','Bihar'),('Chhattisgarh','Chhattisgarh'),('Goa','Goa'),('Gujarat','Gujarat'),('Haryana','Haryana'),
                    ('Himachal Pradesh','Himachal Pradesh'),('Jammu And Kashmir','Jammu And Kashmir'),('Jharkhand','Jharkhand'),('Karnatka','Karnatka'),('Kerala','Kerala'),('Madhya Pradesh','Madhya Pradesh'),('Maharashtra','Maharashtra'),
                    ('Manipur','Manipur'),('Meghalaya','Meghalaya'),('Mizoram','Mizoram'),('Nagaland','Nagaland'),('Odisha','Odisha'),('Punjab','Punjab'),('Rajasthan','Rajasthan'),('Sikkim','Sikkim'),('Tamil Nadu','Tamil Nadu'),
                    ('Telangana','Telangana'),('Tripura','Tripura'),('Uttar Pradesh','Uttar Pradesh'),('Uttarakhand','Uttarakhand'),('West Bengal','West Bengal')]
    property_type = SelectField(u'Property Type', choices = postTypeChoices)
    state = SelectField(u'State', choices = stateChoices,validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    submit = SubmitField('Submit') 

class UpdatePostDetailsForm(FlaskForm):
    postTypeChoices = [('Select','Select'),('1 BHK','1 BHK'),('2 BHK','2 BHK'),('3 BHK','3 BHK'),('4 BHK','4 BHK')]
    stateChoices = [('Select','Select'),('Andhra Pradesh','Andhra Pradesh'),('Arunachal Pradesh','Andhra Pradesh'),('Assam','Assam'),('Bihar','Bihar'),('Chhattisgarh','Chhattisgarh'),('Goa','Goa'),('Gujarat','Gujarat'),('Haryana','Haryana'),
                    ('Himachal Pradesh','Himachal Pradesh'),('Jammu And Kashmir','Jammu And Kashmir'),('Jharkhand','Jharkhand'),('Karnatka','Karnatka'),('Kerala','Kerala'),('Madhya Pradesh','Madhya Pradesh'),('Maharashtra','Maharashtra'),
                    ('Manipur','Manipur'),('Meghalaya','Meghalaya'),('Mizoram','Mizoram'),('Nagaland','Nagaland'),('Odisha','Odisha'),('Punjab','Punjab'),('Rajasthan','Rajasthan'),('Sikkim','Sikkim'),('Tamil Nadu','Tamil Nadu'),
                    ('Telangana','Telangana'),('Tripura','Tripura'),('Uttar Pradesh','Uttar Pradesh'),('Uttarakhand','Uttarakhand'),('West Bengal','West Bengal')]
    tenantChoices = [('Select','Select'),('Family','Family'),('Bachelor','Bachelor')]
    property_type = SelectField(u'Property Type', choices = postTypeChoices, validators = [DataRequired()])
    state = SelectField(u'State', choices = stateChoices, validators = [DataRequired()])
    city = StringField('Price',validators=[DataRequired()])
    tenant = SelectField(u'Tenant', choices = tenantChoices, validators = [DataRequired()])
    address = TextAreaField('Address',validators = [DataRequired(),Length(max=100)] )
    description = TextAreaField('Description',validators = [DataRequired(),Length(max=200)] )
    price = StringField('Price',validators=[DataRequired()])
    submit = SubmitField('Submit') 

    def validate_property_type(self,property_type):
        if property_type.data == 'Select':
            raise ValidationError(' Property Type detail is required. Please select a propety type ')

    def validate_state(self,state):
        if state.data == 'Select':
            raise ValidationError(' State detail is required. Please select a State ')

    def validate_tenant(self,tenant):
        if tenant.data == 'Select':
            raise ValidationError(' Tenant detail is required. Please select a Tenant ')

class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired(),Length(max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(max=25)])
    phone_number = StringField('Contact No.',validators=[DataRequired(),Length(10)])
    submit = SubmitField('Update Profile')
