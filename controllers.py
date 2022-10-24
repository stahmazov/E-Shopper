from app import app
from flask import render_template, request, redirect, flash, url_for, session
from models import *
from extensions import db
from forms import *
from flask_login import login_user, logout_user, login_required, current_user
from flask import json
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from flask_paginate import Pagination, get_page_parameter, get_page_args


@app.context_processor
def category():
    return dict(parents=Category.query.filter(Category.parent_id==None).all(),
                Category=Category, subscribe_form = SubscribeForm())

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template('404.html', description = e.description, status=e.code, name=e.name)

def filter_color(filter_):
    products_color = []

    filter_color = [i[6:] for i in list(filter_.keys()) if i[:5]=='color']
    if not filter_color:
        products_color = 'N/A'
        
    colors = [Color.query.filter(Color.value == i).first() for i in filter_color]
    
    for i in colors:
        products_color.extend(i.products)

    return products_color

def filter_size(filter_):
    products_size = []
    
    filter_size = [i[5:] for i in list(filter_.keys()) if i[:4]=='size']
    if not filter_size:
        products_size = 'N/A'
    
    sizes = [Size.query.filter(Size.value == i).first() for i in filter_size]
    
    for i in sizes:
        products_size.extend(i.products)
        
    return products_size
    
def filter_price(filter_):
    products_price = []
    
    if filter_['min_price']!="" and filter_['max_price']!="":
        products_price = products_price + Product.query.filter(Product.price>int(filter_['min_price'])).\
                filter(Product.price<int(filter_['max_price'])).all()
    elif filter_['min_price']=="" and filter_['max_price'] !="":
        products_price = products_price + Product.query.filter(Product.price<int(filter_['max_price'])).all()
    elif filter_['min_price']!="" and filter_['max_price'] =="":
        products_price = products_price + Product.query.filter(Product.price>int(filter_['min_price'])).all()
    else:
        products_price = 'N/A'
    
    return products_price    

def intersection_(*args):
    args = list(args)
    length = len(args)-1
    while length>=0:
        if not args[length]:
            args.remove(args[length])
        length-=1
    return list(set.intersection(*map(set,args)))

@app.route("/")
def main():
    searched = request.args.get('q')
    filter_ = dict(request.args)
    # print(filter_)
    if searched:
        products = Product.query.filter(Product.name.contains(searched) |\
            Product.description.contains(searched)).all()
    elif (filter_) and (not 'page' in list(filter_.keys())):
        # print(filter_price(filter_))
        # print(filter_color(filter_))
        # print(filter_size(filter_))
        
        color = filter_color(filter_)
        size = filter_size(filter_)
        price = filter_price(filter_)
        
        if (not color) | (not size) | (not price):
            products=[]
        else:     
            if color=='N/A':
                color = []
            if size=='N/A':
                size = []
            if price=='N/A':
                price = []
            
            if (not color) and (not size) and (not price):
                products = Product.query.all()
            else:
                products = intersection_(color, size, price)
    else:
        products = Product.query.all()
    
    sizes = Size.query.order_by(Size.id).all()
    colors = Color.query.order_by(Color.id).all()
    
    product_count = len(products)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 6
    offset = (page-1)*per_page
    
    if page != None:
        x = (int(page) - 1) * per_page
        y = int(page) * per_page
    products = products[x:y]
    
    # print(f'x:{x}, y:{y}, page:{page}, offset:{offset}')
    
    pagination = Pagination(page=page, per_page=per_page, offset=offset,
                            total=product_count, record_name='products')

    return render_template('shop.html', products=products, sizes=sizes, 
                           colors=colors, pagination=pagination)

@app.route("/category/<int:pk>/")
def main_category(pk):
    searched = request.args.get('q')
    filter_ = dict(request.args)

    if searched:
        products = Product.query.filter(Product.name.contains(searched) |\
            Product.description.contains(searched)).all()
        products = intersection_(products, Category.query.filter_by(id=pk).first().products)
        
    elif filter_:
        # print(filter_price(filter_))
        # print(filter_color(filter_))
        # print(filter_size(filter_))
        
        color = filter_color(filter_)
        size = filter_size(filter_)
        price = filter_price(filter_)
        
        if (not color) | (not size) | (not price):
            products=[]
        else:     
            if color=='N/A':
                color = []
            if size=='N/A':
                size = []
            if price=='N/A':
                price = []
            
            if (not color) and (not size) and (not price):
                products = Category.query.filter_by(id=pk).first().products
            else:
                products = intersection_(color, size, price, Category.query.filter_by(id=pk).first().products)
    else:
        products = Category.query.filter_by(id=pk).first().products
    
    sizes = Size.query.order_by(Size.id).all()
    colors = Color.query.order_by(Color.id).all()
    
    product_count = len(products)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 6
    offset = (page-1)*per_page
    
    if page != None:
        x = (int(page) - 1) * per_page
        y = int(page) * per_page
    products = products[x:y]
    
    # print(f'x:{x}, y:{y}, page:{page}, offset:{offset}')
    
    pagination = Pagination(page=page, per_page=per_page, offset=offset,
                            total=product_count, record_name='products')

    return render_template('shop.html', products=products, sizes=sizes, 
                           colors=colors, pagination=pagination)

@app.route("/<int:pk>/", methods=['GET', 'POST'])
def detail(pk):
    form = ReviewForm()
    if request.method =='POST':
        if form.validate_on_submit():
            review = Review(form.comment.data, pk, current_user.id)
            review.save()
            return redirect(url_for('detail', pk = pk))        
    single = Product.query.filter_by(id = pk).first()
    recommendations = Category.query.filter_by(id = single.categories[0].id).first()
    return render_template('detail.html', single=single, recommendations=recommendations, 
                           form=form, users=User)

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if request.method == 'POST':
        if contact_form.validate_on_submit():
            contact_data = Contact(contact_form.name.data, contact_form.email.data,
                                   contact_form.subject.data, contact_form.message.data)
            contact_data.save()
            flash('Contact is saved! Thank you', 'success')
            return redirect(url_for('main'))
    return render_template('contact.html', contact_form=contact_form)

@app.route('/register/',  methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.data)
            user = User(first_name=form.first_name.data, 
                               last_name=form.last_name.data, 
                               email=form.email.data, 
                               password=form.password.data)
            user.save()
            login_user(user)
            flash('Registered successfully!', 'success')
            return redirect(url_for('main'))
    return render_template('register.html', form=form)

@app.route('/login/',  methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Loged in!', 'success')
                return redirect(url_for('main'))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect(url_for('main'))

@app.route('/oopss')
def admin_error():
    return render_template('admin_error.html')

@app.route('/subscribe/', methods=['POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        subscribe_obj = Subscribe(form.data['subscriber_name'], form.data['subscriber_email'])
        try:
            subscribe_obj.save()
            flash('You are subscribed! Thank you', 'success')
        except IntegrityError:
            flash('This e-mail address is already subscribed.', 'info')
    else:
        flash('Please, input correctly!', 'danger')
    return redirect(url_for("main"))

@app.route('/favorites/')
def favorite():
    if not current_user.is_authenticated:
        flash('You should log in for creating a wishlist :)', 'info')
        return redirect(url_for('login'))
    favorites = current_user.favorites
    return render_template('favorites.html', favorites=favorites, Product = Product)

@app.route('/add_favorite/<int:pk>', methods = ['POST'])
def add_favorite(pk):
    if current_user.is_authenticated:
        try:
            favorite_model = Favorite(pk, current_user.id)
            favorite_model.save()
        except IntegrityError:
            flash("Product is already in your wishlist!", 'success')
            return redirect(url_for('detail', pk=pk))
    else:
        flash("You should log in for adding the product to the wishlist...", 'danger')
        return redirect(url_for('login', next=request.url))
    flash("Product is successfully added to your wishlist!", 'success')
    return redirect(url_for('detail', pk=pk))

@app.route('/remove_from_fav/<int:pk>')
def remove_from_fav(pk):
    item = Favorite.query.filter_by(id=pk).first()
    db.session.delete(item)
    db.session.commit()
    flash('The item is successfully deleted!', 'success')
    return redirect(url_for('favorite'))