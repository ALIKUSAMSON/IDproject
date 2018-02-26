from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError, SelectField, FileField
from wtforms.validators import Required, Email, Length, EqualTo, AnyOf, Regexp, Optional
from models import *
from wtforms.fields.html5 import DateField



class RegistrationForm(Form):
    username = StringField('Username',validators=[Required(), Length(min=4,max=18)])
    email = StringField('Email',validators=[Required(),Email(message='Invalid address'),Length(min=1,max=64)])
    role = SelectField('Select User role', choices=(('admin_user','Admin User'),('normal_user','Normal User')))
    password = PasswordField('Password',validators=[Required(), Length(min=6, message="Password must be 6 characters as and more"),EqualTo('confirm',message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class LoginForm(Form):
    username = StringField('Username',validators=[Required(),Length(min=5,max=25)])
    password = PasswordField('Password',validators=[Required(), Length(min=6, message="Password must be 6 characters as and more")])
    submit = SubmitField('Login')


class UploadForm(Form):
    name = StringField('FUll Name',validators=[Required()])
    email = StringField('Email',validators=[Required(),Email(message='Invalid address'),Length(min=1,max=64)])
    position = StringField('Position',validators=[Required()])
    year = DateField('Year of duty',validators=[Required()], format='%Y-%m-%d')
    contact = StringField('Contact',validators=[Required()])
    category = SelectField('Category', choices=(('lc5_chairperson','LC5 chairperson'),('woman_mp','Woman MP'),('woman_counsellor','Woman Counsellor'),
                    ('nrm_mp','NRM Chairperson'),('special_gps','Special GPs'),('er_mp','ER MPs'),('army_mp','ARMY MPs'),
                ('constituency_leader','Constituency Leaders'),('league_leader','Leagues leaders'),('other_leader','Others leaders')))
    submit = SubmitField('upload')


class ImportForm(Form):
    importname = FileField('Browser here')
    submit = SubmitField('upload')




