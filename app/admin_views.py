from datetime import datetime

from wtforms.validators import DataRequired
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.validators import ItemsRequired
from flask_admin.form import rules

from . import admin, db
from .base_admin_views import CustomBaseView
from app.main.models import (
    Category, Post, PostImage,
    Comment, CommentReply
)
from app.auth.models import User, Role


# AUTH BLURPRINT
class UserAdminView(CustomBaseView):

    column_list = ['id', 'email', 'username', 'join_time']
    column_details_exclude_list = ['password', 'avatar_hash']
    column_editable_list = ['email', 'username']
    column_searchable_list = ['email', 'username']
    column_sortable_list = ['id', 'join_time']
    column_default_sort = 'id'

    form_excluded_columns = ['password_hash', 'avatar_hash']
    form_rules = [
        rules.FieldSet(
            ('email', 'username', 'name'), 'Basic Informations',
        ),
        'about_me',
        'location',
        rules.FieldSet(
            ('role', ), 'Roles',
        ),
        'is_active',
    ]
    form_widget_args = {
        'is_active': {
            'column_class': 'form-check',
            'class': 'form-check-input',
            'label_class': 'form-check-label',
        }
    }


admin.add_view(UserAdminView(
            User, db.session, name="User", endpoint="user",
            menu_icon_type="fa", menu_icon_value="fa fa-fw fa-user",
            category="Auth"))

class RoleAdminView(CustomBaseView):

    column_list = ['id', 'name', 'default']

admin.add_view(RoleAdminView(
            Role, db.session, name="Role", endpoint="role",
            menu_icon_type="fa", menu_icon_value="fa fa-fw fa-user-tag",
            category="Auth"))

# MAIN BLURPRINT
class CategoryAdminView(CustomBaseView):

    column_list = ['id', 'name', 'level', 'create_time']
    column_editable_list = ['name']
    column_sortable_list = ['name', 'create_time']
    column_default_sort = 'id'
    column_filters = ['name']
    column_searchable_list = ['name']

    form_columns = ['name', 'level', 'parent', 'posts', 'is_nav']
    form_excluded_columns = ['create_time']
    form_args = {
        'name': {
            'validators': [DataRequired()],
        },
    }
    form_rules = [
        rules.FieldSet(
            ('name', ), 'Name',
        ),
        rules.FieldSet(
            ('parent', 'level'), 'Classification',
        ),
        rules.FieldSet(
            ('posts', ), 'Inclusion',
        ),
        'is_nav'
    ]
    form_widget_args = {
        'is_nav': {
            'column_class': 'form-check',
            'class': 'form-check-input',
            'label_class': 'form-check-label',
        }
    }

admin.add_view(CategoryAdminView(
            Category, db.session, name="Category", endpoint="category",
            menu_icon_type="fa", menu_icon_value="fa fa-fw fa-burn",
            category="Main"))


class PostAdminView(CustomBaseView):

    column_list = ['id', 'title', 'category', 'is_recommend']

admin.add_view(PostAdminView(
            Post, db.session, name="Post", endpoint="post",
            menu_icon_type="fa", menu_icon_value="far fa-fw fa-flag",
            category="Main"))


class PostImageAdminView(CustomBaseView):

    column_list = ['id', 'post_id', 'create_time']

admin.add_view(PostImageAdminView(
            PostImage, db.session, name="PostImage", endpoint="post-image",
            menu_icon_type="fa", menu_icon_value="far fa-fw fa-images",
            category="Main"))


class CommentAdminView(CustomBaseView):

    column_list = ['id', 'user_id', 'post_id', 'status', 'create_time', 'update_time']
    column_formatters = {
        'update_time': lambda v, c, m, p: datetime.strftime(m.create_time, "%Y-%m-%d %H:%M:%S")
    }

admin.add_view(CommentAdminView(
            Comment, db.session, name="Comment", endpoint="comment",
            menu_icon_type="fa", menu_icon_value="far fa-fw fa-comments",
            category="Main"))


class CommentReplyAdminView(CustomBaseView):

    column_list = ['id', 'post_id', 'reply_type', 'create_time']

admin.add_view(CommentReplyAdminView(
            CommentReply, db.session, name="CommentReply", endpoint="comment-reply",
            menu_icon_type="fa", menu_icon_value="far fa-fw fa-comment-dots",
            category="Main"))