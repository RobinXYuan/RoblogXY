from flask import render_template
from flask.views import View


class BaseView(View):
    template_name = None
    site_title = "RoblogXY Admin"
    site_footer = "Power by Xiaorong YUAN 2019-2020"
    object_name = "object"
    model = None


    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = {
            self.object_name: self.get_objects(),
            'site_title': self.site_title,
            'site_footer': self.site_footer
        }
        return self.render_template(context)

    def get_objects(self):
        return self.model.query.all()