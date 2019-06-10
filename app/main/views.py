from datetime import datetime

from flask import render_template, url_for, request, abort
from flask import views
from flask_login import current_user, login_required

from app import db
from app.main import main
from .models import (
    CategoryLevels,
    Category, Post, PostImage,
    Comment, CommentReply
)


class IndexView(views.MethodView):
    
    def get(self):
        categories = Category.query\
                        .filter_by(level=CategoryLevels.LEVEL_I)\
                        .filter_by(is_nav=True)\
                        .all()
        return render_template('main/index.html', categories=categories, is_index=True)


class CategoryView(views.MethodView):

    def get(self):
        return render_template('main/categories.html')


class PostsView(views.MethodView):

    def get(self):
        return render_template('main/posts.html')


main.add_url_rule('/', view_func=IndexView.as_view('index'))
main.add_url_rule('/category', view_func=CategoryView.as_view('category'))
main.add_url_rule('/post', view_func=PostsView.as_view('post'))