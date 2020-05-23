from flask import render_template,url_for,flash,request,redirect
from app import app, db , bcrypt
from app.form import RegistrationForm,LoginForm,PostAddForm
from app.models import User,Property,propertyImages
from flask_login import login_user ,logout_user,current_user
import os

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
            return redirect(url_for('dashboard'))
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

@app.route('/upload', methods=['POST'])
def handle_upload():
    print(request.form.get('files'))
    for key, f in request.files.items():
        if key.startswith('file'):
            return f.filename
            # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    form = PostAddForm()
    if(form.validate_on_submit()):
        ads = Property(state = form.state.data ,city = form.city.data ,address = form.address.data ,description = form.description.data ,price = form.price.data,user_id=current_user.id)
        db.session.add(ads)
        db.session.commit()
        print(form.address.data)
        property_id = Property.query.filter_by(address=form.address.data).first()
        print(property_id.id)
        for key, f in request.files.items():
            print(property_id.id)
            if key.startswith('file') and property_id.id:
                print('working')
                upload = propertyImages(filename=f.filename)
                db.session.add(upload)
                db.session.commit()
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('dashboard.html',title='Dashboard', form=form)

@app.route('/sidedash')
def sidedash():
    return render_template('sidedash.html')

@app.route('/sidepost')
def sidepost():
    if(request.method == 'POST'):
        print(request.files)
    return render_template('sidepost.html')

@app.route('/sideupdate')
def sideupdate():
    return render_template('sideupdate.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))