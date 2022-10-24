from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import url_for, request, redirect
import flask_admin as admin
from flask_admin import helpers, expose

     
# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        elif not current_user.is_superuser:
            return redirect(url_for('admin_error'))
        return super(MyAdminIndexView, self).index()