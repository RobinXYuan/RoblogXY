# from flask import render_template, redirect, abort, flash, url_for
# from flask.views import View, MethodView
# from flask_login import login_required, login_user, logout_user

# from app.decorators import admin_required
# from app.auth.models import User, Role, Permission
# from app.main.models import (
#     Category, CategoryLevels, Post, 
#     PostImage, Comment, CommentStatus,
#     CommentReply
# )
# from . import admin
# from .forms import AdminLoginForm
# from .admin_base_views import BaseAdminView, site


# class AdminLogin(View):
#     methods = ['GET', 'POST']

#     def dispatch_request(self):
#         form = AdminLoginForm()
#         if form.validate_on_submit():
#             user = User.query.filter_by(email=form.email.data).first()
#             if user is not None and user.verify_password(form.password.data):
#                 if user.is_administrator():
#                     login_user(user, form.remember_me.data)
#                     return redirect(url_for('admin.index'))
#                 abort(403)
#             flash('Invalid form information')
#         return render_template('admin_login.html', form=form)

# admin.add_url_rule('/login', view_func=AdminLogin.as_view('login'))


# class CategoryAdminView(BaseAdminView):

#     list_display = ['name', 'level', 'create_time', ]

#     def get_objects(self):
#         return Category.query.all()

#     # def dispatch_request(self):
#     #     context = super().get_context()
#     #     context.update({
#     #         'objects': self.get_objects(),
#     #     })
#     #     return self.render_template(context)

# site.register(CategoryAdminView, Category, blp_name="main")


# class PostAdminView(BaseAdminView):
#     model = Post

# # admin.add_url_rule('/post', view_func=CategoryAdminView.as_view('post'))
# site.register(PostAdminView, Post, blp_name="main")