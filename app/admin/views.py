from flask import render_template, redirect, abort, flash, url_for
from flask_login import login_required

from app.decorators import admin_required
from app.auth.models import User
from . import admin
from .forms import AdminLoginForm


@admin.route('/login', methods=['GET', 'POST'], endpoint='login')
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            if user.is_administrator():
                return redirect(url_for('admin.index'))
            abort(403)
        flash('Invalid form information')
    return render_template('admin_login.html', form=form)


@admin.route('/', methods=['GET', 'POST'], endpoint='index')
def admin_index():
    return render_template('admin_index.html')