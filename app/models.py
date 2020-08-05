from datetime import datetime
from app import db, login_manager  
from flask_login import  UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(25),nullable=False)
    middle_name = db.Column(db.String(25),nullable=True)
    last_name = db.Column(db.String(25),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    username = db.Column(db.String(25),nullable=True,unique=True)
    phone_number = db.Column(db.String(10),nullable=False)
    profile_image = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(1000),nullable=False)
    posts = db.relationship('Property',backref="owner",lazy=True)
    date_of_creation =  db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}'),{self.first_name + self.last_name},{self.email},{self.phone_number},"

class Property(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    user_id  = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    type = db.Column(db.String(25),nullable=False,unique=False)
    state = db.Column(db.String(25),nullable=False,unique=False)
    city = db.Column(db.String(25),nullable=False,unique=False)
    tenant = db.Column(db.String(25),nullable=False,unique=False)
    address = db.Column(db.String(25),nullable=False,unique=True)
    description = db.Column(db.String(50),nullable=False,unique=True)
    price = db.Column(db.String(25),nullable=False,unique=False)
    upload = db.relationship('propertyImages',backref="propertyUpload",lazy=True)
    impression = db.relationship('Impression',backref="impressionUser",lazy=True)
    date_of_creation =  db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"Property('{self.state}'),{self.city + self.address},{self.description},{self.price},"

class propertyImages(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String(50),nullable=False)
    property_id = db.Column(db.Integer,db.ForeignKey('property.id'),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    date_of_creation =  db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"propertyimages('{self.filename},{self.property_id},{self.user_id}'),"

class Impression(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    property_id = db.Column(db.Integer,db.ForeignKey('property.id'),nullable=False)
    status = db.Column(db.String(50),nullable=False)
    date_of_creation =  db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"impression('{self.id},{self.user_id},{self.status}')"