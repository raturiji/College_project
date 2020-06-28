from flask import render_template,url_for,flash,request,redirect,session
from app import app, db , bcrypt
from app.form import RegistrationForm,LoginForm,PostAddForm
from app.models import User,Property,propertyImages
from flask_login import login_user ,logout_user,current_user
from sqlalchemy import and_,or_ 
import os
import time
import secrets


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

@app.route('/search',methods=['GET','POST'])
def search():
    if(request.method == "POST"):
        print(request.form['type'])
        print(request.form['state'])
        print(request.form['city'])
        if(request.form['type'] == ''):
            # data = Property.query.filter_by(city=request.form['city'],state=request.form['state']).all()
            city = "%{}%".format(request.form['city'])
            state = "%{}%".format(request.form['state'])
            data = Property.query.filter(and_(Property.city.like(city),Property.state.like(state))).all()
        else:
            city = "%{}%".format(request.form['city'])
            type = "%{}%".format(request.form['type'])
            state = "%{}%".format(request.form['state'])
            data = Property.query.filter(and_(Property.city.like(city),Property.state.like(state),Property.type.like(type))).all()
        return render_template('searchList.html',title='Search',data=data,propertyImages = propertyImages)
    return render_template('searchList.html',title='Search')



@app.route('/upload', methods=['GET','POST'])
def handle_upload():
    print('working')   
    for key, f in request.files.items():
        if key.startswith('file'):
            random_hex = secrets.token_hex(8)
            _,f_ext = os.path.splitext(f.filename)
            filename = random_hex + f_ext
            upload = propertyImages(filename=filename,property_id=session['property_id'],user_id=current_user.id)
            db.session.add(upload)
            db.session.commit()
            f.save(os.path.join(app.config['UPLOADED_PATH'],filename))
    isUploaded = propertyImages.query.filter_by(property_id=session['property_id']).first()
    if(isUploaded):
        flash(f'Post Added Successfully','success')
        return redirect(url_for('dashboard'))
    return render_template('handle-upload.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html',title='Dashboard')



@app.route('/postadd',methods=['GET','POST'])
def postadd():
    form = PostAddForm()
    if(form.validate_on_submit()):
        ads = Property(type = form.property_type.data ,state = form.state.data ,city = form.city.data ,tenant = form.tenant.data ,address = form.address.data ,description = form.description.data ,price = form.price.data,user_id=current_user.id)
        db.session.add(ads)
        db.session.commit()
        print(form.address.data)
        property_id = Property.query.filter_by(address=form.address.data).first()
        session['property_id'] = property_id.id
        return redirect(url_for('handle_upload'))
    return render_template('postadd.html',title='Dashboard', form=form)

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