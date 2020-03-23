from flask import render_template,url_for,flash,redirect
from app import app, db , bcrypt
from app.form import RegistrationForm,LoginForm
from app.models import User
from flask_login import login_user ,logout_user,current_user

dummy_user = {'email':'sagar@gmail.com','password':'12345678'}
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user.password)
        if user and  bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull! Please check email and password again.', 'danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, phone_number=form.phone_number.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.first_name.data} successfully','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Sign Up',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))