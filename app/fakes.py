import os
import random
from datetime import datetime

from PIL import Image
from faker import Faker

from flask import current_app
from sqlalchemy.exc import IntegrityError

from app import db
from app.auth.models import User
from app.main.models import Category, CategoryLevels, Post


fake = Faker()

def fake_posts(count):
    categories = Category.query.filter_by(level=CategoryLevels.LEVEL_III).all()
    user = User.query.filter_by(email='robinxyuan@yeah.net').first()
    for i in range(count):
        category = random.choice(categories)
        post = Post(
            title=' '.join(fake.words(nb=random.randint(5, 15))),
            content='\n'.join(fake.paragraphs(nb=random.randint(5, 10))),
        )
        post.category = category
        post.author = user.id
        db.session.add(post)