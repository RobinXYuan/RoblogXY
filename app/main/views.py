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


class PostsView(views.MethodView):

    def get(self):
        categories = Category.query\
                        .filter_by(level=CategoryLevels.LEVEL_I)\
                        .filter_by(is_nav=True)\
                        .all()
        cats = Category.query\
                        .filter_by(level=CategoryLevels.LEVEL_I)\
                        .all()
        cat_id = request.args.get('cat')
        subcat_id = request.args.get('subcat')
        if cat_id:
            third_cats = Category.query.get(cat_id).children
            query = [c.posts for c in third_cats]
        else:
            third_cats = []
            query = Post.query.all()

        context = {
            'categories': categories,
            'cats': cats,
            'third_cats': third_cats,
            'query': query,
            'cat_id': cat_id,
            'subcat_id': subcat_id,
        }
        return render_template('main/posts.html', **context)


main.add_url_rule('/', view_func=IndexView.as_view('index'))
main.add_url_rule('/posts', view_func=PostsView.as_view('posts'))