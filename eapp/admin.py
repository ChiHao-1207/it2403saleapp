from flask_admin.contrib.sqla import ModelView
from eapp.models import Category, Product
from flask_admin import Admin, BaseView, expose, AdminIndexView
from eapp import app, db, dao
from flask_login import logout_user, current_user
from eapp.models import UserRoleEnum
from flask import redirect

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        # [(1, 'Mobile', 6), (2, 'Tablet', 3), (3, 'Laptop', 0), (4, 'Desktop', 0)]
        return self.render('admin/index.html', stats=dao.count_product_by_cate())

admin = Admin(app=app, name="E-commerce's Admin", index_view=MyAdminIndexView())

class AdminModelView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class AuthenticatedView(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated


class ProductView(AdminModelView):
    column_list = ['id', 'name', 'price', 'category_id']
    column_searchable_list = ['name']
    can_export = True
    column_filters = ['name', 'price']
    edit_modal = True
    column_editable_list = ['name']


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(AdminModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))