import click

from flask import Flask, render_template
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

from config import config


admin = Admin(
    name="RoblogXY Admin",
    category_icon_classes={
        'Auth': 'fa fa-fw fa-user-secret',
        'Main': 'fas fa-fw fa-dharmachakra'
    }
)
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    from .base_admin_views import CustomAdminIndexView

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    admin.init_app(app, index_view=CustomAdminIndexView(
        menu_icon_type="fa",
        menu_icon_value="fa fa-fw fa-home"))
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return None
    register_commands(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def register_commands(app):
    @app.cli.command()
    @click.option('--count', default=100, help='Create fake posts, default count is 100')
    def fakeposts(count):
        from .fakes import fake_posts
        fake_posts(count)
        db.session.commit()


from .admin_views import *