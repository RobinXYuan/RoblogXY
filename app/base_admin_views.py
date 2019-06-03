from datetime import datetime

from flask import (
    url_for, redirect, render_template,
    flash, abort
)
from flask_admin import AdminIndexView
from flask_admin import helpers, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user

from app.auth.models import User
from .admin_forms import AdminLoginForm


class CustomAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_administrator():
            return redirect(url_for('.login'))
        return self.render('site_admin/admin_index.html')

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        form = AdminLoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.verify_password(form.password.data):
                if user.is_administrator():
                    login_user(user, form.remember_me.data)
                    return redirect(url_for('admin.index'))
                abort(403)
            flash('Invalid form information')
        return render_template('site_admin/admin_login.html', form=form)

    @expose('/logout')
    def logout(self):
        logout_user()
        return redirect(url_for('admin.login'))


class CustomBaseView(ModelView):

    list_template = "site_admin/admin_list.html"
    create_template = "site_admin/admin_add.html"
    edit_template = "site_admin/admin_detail.html"
    site_footer = "Power by Robin.X.Yuan 2019 - 2020".upper()

    column_formatters = {
        'create_time': lambda v, c, m, p: datetime.strftime(m.create_time, "%Y-%m-%d %H:%M:%S")
    }

    def is_accessible(self):
        return current_user.is_administrator()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login'))