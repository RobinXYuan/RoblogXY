# from collections import namedtuple

# from flask import render_template, url_for, g
# from flask.views import View

# from . import admin


# class AdminView:
    
#     def __init__(self):
#         self._admin_site = namedtuple(
#                                 'ADMIN_SITE',
#                                 'admin_class model_class blp_name url')
#         self._admin_sites = []

#     def register(self, admin_class, model_class, **options):
#         mclass_name = model_class.__name__.lower()
#         admin.add_url_rule(
#                 f'/{mclass_name}',
#                 view_func=admin_class.as_view(mclass_name),
#                 methods=['GET', 'POST'])
#         site = self._admin_site(
#                     admin_class=admin_class,
#                     model_class=model_class,
#                     blp_name=options["blp_name"],
#                     url=f'/admin/{mclass_name}')
#         self._admin_sites.append(site)

#     def get_admin_sites(self):
#         return self._admin_sites

# site = AdminView()


# class BaseSiteView(View):
#     template_name = None
#     site_title = "RoblogXY Admin"
#     site_footer = "Power by Xiaorong YUAN 2019-2020"
#     list_display = []

#     def get_template_name(self):
#         return self.template_name

#     def render_template(self, context):
#         return render_template(self.get_template_name(), **context)

#     def dispatch_request(self):
#         context = self.get_context()
#         return self.render_template(context)

#     def get_context(self):
#         return {
#             'objects': self.get_objects(),
#             'field_list': self.list_display,
#             'sidebar_items': self._get_register_sites(),
#             'site_title': self.site_title,
#             'site_footer': self.site_footer
#             }

#     def get_objects(self):
#         raise NotImplementedError('This method has not be implemented!')

#     def _get_register_sites(self):
#         reg_sites = site.get_admin_sites()
#         all_sites = dict()
#         for reg_site in reg_sites:
#             klass_name = reg_site.model_class.__name__
#             klass_url = reg_site.url
#             s = {
#                 'name': klass_name,
#                 'url': reg_site.url
#             }
#             blp_name = reg_site.blp_name.upper()
#             if blp_name in all_sites.keys():
#                 all_sites[blp_name].append(s)
#             else:
#                 all_sites[blp_name] = [s]
#         return all_sites


# class IndexAdminView(BaseSiteView):
#     template_name = "admin_index.html"

# admin.add_url_rule('/', view_func=IndexAdminView.as_view('index'))


# class BaseAdminView(BaseSiteView):
#     template_name = "admin_list.html"