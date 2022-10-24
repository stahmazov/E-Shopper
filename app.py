from flask import Flask

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:12345@127.0.0.1:5432/shopper'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@127.0.0.1:3306  /shopper'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'flask_project'
app.config['FLASK_ADMIN_SWATCH'] = 'superhero'


from models import *
from controllers import *


if ('__name__') == ('__main__'):
    app.init_app(db)
    app.init_app(migrate)