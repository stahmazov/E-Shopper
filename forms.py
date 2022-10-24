from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class ContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()],
                       render_kw={'placeholder':"Your full name*",
                                  'class':"form-control"})
    email = StringField('email', validators=[DataRequired(), Email()],
                       render_kw={'placeholder':"Your email*",
                                  'class':"form-control"})
    subject = StringField('subject', validators=[DataRequired()],
                        render_kw={'placeholder':'Subject',
                                    'class':"form-control"})
    message = TextAreaField('message', validators=[DataRequired(), Length(min=10, max=250)],
                          render_kw={'placeholder':'Message',
                                     'class':"form-control"})
    submit = SubmitField('Send Message', render_kw={'class':"btn btn-primary py-2 px-4"})
    
    
class RegisterForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired(), Length(min=3, max=50)],
                       render_kw={'placeholder':"First name",
                                  'class':"form-control"})
    last_name = StringField('last_name', validators=[DataRequired(), Length(min=3, max=50)],
                       render_kw={'placeholder':"Last name",
                                  'class':"form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={'placeholder':"Email",
                                  'class':"form-control"})
    password = StringField('password', validators=[DataRequired(), Length(min=8, max=30)],
                       render_kw={'placeholder':"Password", "type":"password",
                                  'class':"form-control"})
    confirm = StringField('confirm', validators=[DataRequired(), Length(min=8, max=30),
                                                 EqualTo('password')],
                       render_kw={'placeholder':"Confirm Password", "type":"password",
                                  'class':"form-control"})
    submit = SubmitField('Register', render_kw={'class':"btn btn-primary py-2 px-4"})


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={'placeholder':"Your email", 'class':"form-control"})
    password = StringField('password', validators=[DataRequired(), Length(min=8, max=30)],
                       render_kw={'placeholder':"Your password", "type":"password",
                                  'class':"form-control"})
    submit = SubmitField('Login', render_kw={'class':'btn btn-primary py-2 px-4'})
    
    
class ReviewForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=10, max=150)],
                        render_kw={'class':"form-control"})
    submit = SubmitField('Leave Your Review', render_kw={'class':'btn btn-primary py-2 px-4'})
    
    
class FilterForm(FlaskForm):
    price = BooleanField('Price', render_kw={'class':"form-control"})
    color = BooleanField('Color', render_kw={'class':"form-control"})
    size = BooleanField('Size', render_kw={'class':"form-control"})
    submit = SubmitField('Submit', render_kw={'class':'btn btn-primary py-2 px-4'})
    
class SubscribeForm(FlaskForm):
    subscriber_name = StringField('subscriber_name', validators=[DataRequired(), Length(min=3, max=50)],
                       render_kw={'placeholder':"Your name",
                                  'class':"form-control"})
    
    subscriber_email = StringField('subscriber_email', validators=[DataRequired(), Email()],
                        render_kw={'placeholder':"Your email",
                                  'class':"form-control",
                                  'type':'email'})
    subscribe_submit = SubmitField('Submit', render_kw={'class':'btn btn-primary btn-block border-0 py-3'})
    
