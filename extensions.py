from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from admin import MyAdminIndexView

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
admin = Admin(app, name='Shopper', template_mode='bootstrap3', index_view=MyAdminIndexView())
