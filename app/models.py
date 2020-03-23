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
    date_of_creation =  db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}'),{self.first_name + self.last_name},{self.email},{self.phone_number},"