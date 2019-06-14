from flask import views
from flask import render_template

from app.main.models import Category, CategoryLevels


class BaseView(views.View):
    template_name = None

    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = self.get_context()
        return self.render_template(context)

    def get_context(self):
        cats = Category.query\
                        .filter_by(level=CategoryLevels.LEVEL_I)\
                        .all()
        categories = list(filter(lambda x: x.is_nav==True, cats))
        return {
            'cats': cats,
            'categories': categories
        }
