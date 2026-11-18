import math

from flask import render_template, request, redirect
from flask_login import login_user, logout_user
from eapp import app, dao, login


@app.route("/")
def index():
    products = dao.load_products(kw=request.args.get('kw'),
                                 cate_id=request.args.get('category_id'),
                                 page=int(request.args.get('page', 1)))
    page_size = app.config['PAGE_SIZE']
    return render_template('index.html', products=products, pages=math.ceil(dao.count_products()/page_size))


@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.authenticate(username=username, password=password)
    if u:
        login_user(user=u)

    next = request.args.get('next')
    if next:
        return redirect(next)

    return redirect('/admin')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['post'])
def register_process():
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    err_msg = None
    if not password or not confirm or password != confirm:
        err_msg = 'Mật khẩu KHÔNG khớp!'
    else:
        pass

    return render_template('register.html', err_msg=err_msg)

@app.route('/logout')
def logout_view():
    logout_user()
    return redirect('/login')

@app.context_processor
def common_responses():
    categories = dao.load_categories()

    return {
        'categories': categories
    }

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    with app.app_context():
        from eapp import admin
        app.run(debug=True)
