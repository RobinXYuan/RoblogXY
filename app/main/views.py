from datetime import datetime

from flask import url_for, request, abort, current_app
from flask_login import current_user, login_required

from app import db
from app.main import main
from app.views import BaseView
from .models import (
    CategoryLevels,
    Category, Post, PostImage,
    Comment, CommentReply
)


class IndexView(BaseView):

    template_name = 'main/index.html'

    def dispatch_request(self):
        context = super().get_context()
        context.update({
            'is_index': True
        })
        return self.render_template(context)


class PostsView(BaseView):

    template_name = 'main/posts.html'

    def dispatch_request(self):
        context = super().get_context()

        cat_id = request.args.get('cat')            # 第二级目录
        subcat_id = request.args.get('subcat')      # 第三级目录
        rmd = request.args.get('rmd')               # 推荐文章
        read = request.args.get('read')             # 阅读数量排序
        time = request.args.get('time')             # 创建时间排序
        desc = request.args.get('desc')             # 是否倒序

        cat = None
        subcat = None

        if cat_id:
            cat = Category.query.get(cat_id)
            third_cats = cat.children
            if subcat_id:
                subcat = list(filter(lambda x: int(x.id)==int(subcat_id), third_cats))[0]
                query = subcat.posts
            else:
                query = Post.query.join(Category, Post.category_id==Category.id).filter(Category.parent_id==cat_id)
        else:
            third_cats = []
            query = Post.query

        if rmd:
            query = query.filter(Post.is_recommend==True)

        if time:
            query = query.order_by(Post.create_time)
        elif read:
            if desc:
                query = query.order_by(Post.read_times.desc())
            else:
                query = query.order_by(Post.read_times)
        else:
            query = query.order_by(Post.create_time.desc())
        

        page = request.args.get('page', 1, type=int)
        pagination = query.paginate(
            page, per_page=current_app.config['ROBLOGXY_POSTS_PER_PAGE'],
            error_out=False
        )

        posts = pagination.items

        context.update({
            'third_cats': third_cats,
            'posts': posts,
            'pagination': pagination,
            'cat': cat,
            'subcat': subcat,
            'rmd': rmd,
            'read': read,
            'time': time,
            'desc': desc
        })

        return self.render_template(context)


class PostView(BaseView):

    template_name = 'main/post.html'
    methods = ['GET', 'POST']

    def dispatch_request(self, post_id):
        context = super().get_context()

        post = Post.query.get(post_id)

        context.update({
            'post': post
        })

        return self.render_template(context)


main.add_url_rule('/', view_func=IndexView.as_view('index'))
main.add_url_rule('/posts', view_func=PostsView.as_view('posts'))
main.add_url_rule('/post/<int:post_id>', view_func=PostView.as_view('post'))