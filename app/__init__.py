
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager  
from flask_dropzone import Dropzone  
#from flask_uploads import UploadSet, configure_uploads,IMAGES,patch_request_class
import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__)
app.config['UPLOADED_PATH']=os.path.join(basedir, 'uploads')
app.config['SECRET_KEY'] = 'b23b76c2836adb89eb1bddb42e761166'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/db_test'
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*,.jpg'
app.config['DROPZONE_UPLOAD_ON_CLICK']=True
app.config['DROPZONE_IN_FORM']=True
app.config['DROPZONE_AUTO_PROCESS_QUEUE'] = False
app.config['DROPZONE_UPLOAD_ACTION']='dashboard' # URL or endpoint
app.config['DROPZONE_UPLOAD_BTN_ID']='submit'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) 
dropzone = Dropzone(app)
print(app.config['UPLOADED_PATH'])


from app import routes