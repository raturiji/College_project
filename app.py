from datetime import datetime
from flask import Flask,render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from form import RegistrationForm,LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b23b76c2836adb89eb1bddb42e761166'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/db_test'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(25),nullable=False)
    middle_name = db.Column(db.String(25),nullable=True)
    last_name = db.Column(db.String(25),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    username = db.Column(db.String(25),nullable=True,unique=True)
    phone_number = db.Column(db.String(10),nullable=False)
    profile_image = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(20),nullable=False)
    date_of_creation =  db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}'),{self.first_name + self.last_name},{self.email},{self.phone_number},"




dummy_user = {'email':'sagar@gmail.com','password':'12345678'}
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.email.data==dummy_user['email']) and (form.password.data==dummy_user['password']):
            flash(f'Account login for {form.email.data} successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull! Please check email and password again.', 'danger')

    return render_template('login.html',title='Login',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.first_name.data} successfully','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Sign Up',form=form)

if __name__ == '__main__':
    app.run(debug=True)
