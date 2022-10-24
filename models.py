from extensions import db, login_manager, admin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_admin.contrib.sqla import ModelView

class SaveModel:
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
class User(UserMixin, db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_superuser = db.Column(db.Boolean)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    favorites = db.relationship("Favorite", backref="user")
    
    def __init__(self, first_name, last_name, email, password, is_superuser=False):
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.password=generate_password_hash(password)
        self.is_superuser=is_superuser
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

        
product_category = db.Table('product_category',
                    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                    )
        
        
class Category(db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    parent = db.relationship('Category', remote_side=id)
    
    
    products = db.relationship(
        "Product", secondary=product_category, back_populates="categories"
    )
    
    def __init__(self, name, parent_id):
        self.name = name
        self.parent_id=parent_id
        
    def __repr__(self):
        return self.name
    
    
product_color = db.Table('product_color',
                    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                    db.Column('color_id', db.Integer, db.ForeignKey('color.id'))
                    )

product_size = db.Table('product_size',
                    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                    db.Column('size_id', db.Integer, db.ForeignKey('size.id'))
                    )

class Product(db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(155), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Numeric(10,2), nullable=False)
    discounted_price = db.Column(db.Numeric(10,2))
    discount = db.Column(db.Numeric(10,2))
    discount_rate = db.Column(db.Numeric(10,2))
    choice_relative = db.Column(db.Boolean)
    main_image = db.Column(db.String(155))
    images = db.relationship('ProductImage', backref='ProductImage')
    colors = db.relationship(
        "Color", secondary=product_color, back_populates="products"
    )
    sizes = db.relationship(
        "Size", secondary=product_size, back_populates="products"
    )
    reviews = db.relationship('Review', backref='Review')
    categories = db.relationship(
        "Category", secondary=product_category, back_populates="products"
    )
    
    def __init__(self, name, description, price, main_image,choice_relative,
                 discounted_price,
                 discount=0, discount_rate=0):
        self.name = name
        self.description = description
        self.price = price
        self.main_image = main_image
        self.choice_relative = choice_relative
        self.discount = discount
        self.discount_rate = discount_rate
        self.discounted_price = self.get_discounted_price(self.price)
        
    def get_discounted_price(self):
        if self.choice_relative:
            return self.price - (self.price * self.discount_rate)
        else:
            return self.price-self.discount    
        
    def __repr__(self):
        return self.name
    

class ProductImage(db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(155), unique=True, nullable=False)
    variation_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    def __init__(self, name, variation_id):
        self.name = name
        self.variation_id = variation_id
        
    def __repr__(self):
        return self.name
    

class Color(db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(25), unique=True, nullable=False)
    products = db.relationship(
        "Product", secondary=product_color, back_populates="colors"
    )
    
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return self.value


class Size(db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(5), unique=True, nullable=False)
    products = db.relationship(
        "Product", secondary=product_size, back_populates="sizes"
    )
    
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return self.value
    

    
class Review(db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime(), default = datetime.now())
    variation_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, comment, variation_id, user_id):
        self.comment = comment
        self.variation_id = variation_id
        self.user_id = user_id
        
    def __repr__(self):
        return f"{self.comment[:30]}..."
    
class Contact(db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    
    def __init__(self, name, email, subject, message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        
    def __repr__(self):
        return self.subject


class Subscribe(db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    
    def __init__(self, full_name, email):
        self.full_name = full_name
        self.email = email
        
    def __repr__(self):
        return self.full_name
    
    
class Favorite(db.Model, SaveModel):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship("Product", backref="Product")
    
    def __init__(self, product_id, user_id):
        self.product_id = product_id
        self.user_id = user_id
        
    def __repr__(self):
        return f"{self.product_id} of {self.user_id}"
    
    
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(ProductImage, db.session))
admin.add_view(ModelView(Color, db.session))
admin.add_view(ModelView(Size, db.session))
admin.add_view(ModelView(Review, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(Subscribe, db.session))
admin.add_view(ModelView(Favorite, db.session))