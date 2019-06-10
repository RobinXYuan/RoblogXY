import enum
from datetime import datetime

from app import db
from app.auth.models import User


class CategoryLevels(enum.Enum):
    LEVEL_I = 0
    LEVEL_II = 1
    LEVEL_III = 2


class Category(db.Model):

    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    level = db.Column(db.Enum(CategoryLevels))
    description = db.Column(db.String(255))
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)

    is_nav = db.Column(db.Boolean, default=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    parent = db.relationship('Category', remote_side=[id])
    
    posts = db.relationship('Post', backref="category", lazy='dynamic')

    @property
    def children(self):
        return Category.query.filter(Category.parent_id==self.id).all()

    def __repr__(self):
        return f"<Category {self.name} ({self.level})>"


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    is_recommend = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)
    read_times = db.Column(db.Integer, default=0)

    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    comments = db.relationship('Comment', backref="post")
    images = db.relationship('PostImage', backref="post")

    def __repr__(self):
        return f'<Post {self.title}>'


class PostImage(db.Model):
    __tablename__ = "post_images"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PaperImage {self.id} for {self.post_id}>"


class CommentStatus(enum.Enum):
    NORMAL = 0
    FORBID = 1
    DELETE = 2


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2048))
    status = db.Column(db.Enum(CommentStatus))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    replies = db.relationship('CommentReply', backref="comment")

    def __repr__(self):
        return f"<Comment to {self.post_id} by {self.user_id}>"


class ReplyTypes(enum.Enum):
    LIKE = 0
    DISLIKE = 1
    TEXT = 2


class CommentReply(db.Model):
    __tablename__ = "comment_replies"
    id = db.Column(db.Integer, primary_key=True)
    reply_type = db.Column(db.Enum(ReplyTypes))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    
    def __repr__(self):
        return f"<Reply to {self.comment_id} with {self.reply_type}>"