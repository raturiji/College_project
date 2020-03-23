
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager    

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b23b76c2836adb89eb1bddb42e761166'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/db_test'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) 

from app import routes