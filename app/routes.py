from flask import render_template,url_for,flash,request,redirect,session
from app import app, db , bcrypt
from app.form import RegistrationForm,LoginForm,PostAddForm
from app.models import User,Property,propertyImages, Impression
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

@app.route('/impression')
def impression():
    if current_user.is_authenticated:
        data = Property.query.filter_by(user_id=current_user.id)
    return render_template('impression.html',data=data,Impression=Impression,User=User)

@app.route('/updateProperty')
def updateProperty():
    if current_user.is_authenticated:
        data = Property.query.filter_by(user_id=current_user.id).all()
        return render_template('update-property.html',data=data,propertyImages=propertyImages)
    return render_template('dashboard.html')

@app.route('/updateImages/<int:id>/<string:status>',methods=['GET','POST'])
def updateImages(id,status):
    print('checking')
    session['property_id'] = id
    if current_user.is_authenticated:
        if status=='uploaded':
            for key, f in request.files.items(): 
                if key.startswith('file'):
                    random_hex = secrets.token_hex(8)
                    _,f_ext = os.path.splitext(f.filename)
                    filename = random_hex + f_ext
                    print(id)
                    print('reach')
                    upload = propertyImages(filename=filename,property_id=id,user_id=current_user.id)
                    print(upload)
                    db.session.add(upload)
                    db.session.commit()
                    f.save(os.path.join(app.config['UPLOADED_PATH'],filename))
        else:
            return render_template('update-images.html',id=id)
        flash(f'Images Update Successfully','success')
        return redirect(url_for('updateProperty'))    

@app.route('/deleteImage/<int:id>')
def deleteImage(id):
    if current_user.is_authenticated:
        print(id)
        propertyImages.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('updateProperty'))
   

@app.route('/handleImpression/<int:id>/<string:action>')
def handleImpression(id,action):
    if current_user.is_authenticated:
        print(id)
        print(action)
        if action == 'accept':
            Impression.query.filter_by(id=id).update(dict(status='Accepted'))
            db.session.commit()
        else:
            Impression.query.filter_by(id=id).delete()
            db.session.commit()
        data = Property.query.filter_by(user_id=current_user.id)
    return render_template('impression.html',data=data,Impression=Impression,User=User)

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

@app.route('/sendImpression/<string:propertyId>/<string:city>/<string:state>')
def sendImpression(propertyId,city,state):
    if current_user.is_authenticated:
        print(propertyId)
        print(city)
        print(state)
        print(User.id)
        redirectCity = "%{}%".format(city)
        redirectState = "%{}%".format(state)
        data = Property.query.filter(and_(Property.city.like(city),Property.state.like(state))).all()
        impressions = Impression(user_id=current_user.id, property_id=propertyId, status='Pending')
        db.session.add(impressions)
        db.session.commit()
        flash(f'Your impression has been recorded to the owner','success')
        return render_template('searchList.html',title='Search',data=data,propertyImages = propertyImages)
    else:
        return redirect('home')

# @app.route('/sendImpression')
# def sendImpression():
#     if current_user.is_authenticated:
#         print(propertyId)
#         print(city)
#         print(type)
#     else:
#         return redirect('home')

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