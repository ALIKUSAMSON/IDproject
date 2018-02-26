from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from run import *
from forms import *

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	role = db.Column(db.String(120), index=True)
	password = db.Column(db.String(120), index=True,)

	def is_authenticated(self):
		return True
 
 	def is_active(self):
 		return True
 
 	def is_anonymous(self):
 		return False
 
 	def get_id(self):
 		return unicode(self.id)
 
 	def __repr__(self):
 		return '<User %r>' % (self.username)


class Admin(UserMixin, db.Model):
	__tablename__ = 'admin_users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	role = db.Column(db.String(120), index=True)
	password = db.Column(db.String(120), index=True,)

	def is_authenticated(self):
		return True
 
 	def is_active(self):
 		return True
 
 	def is_anonymous(self):
 		return False
 
 	def get_id(self):
 		return unicode(self.id)
 
 	def __repr__(self):
 		return '<User %r>' % (self.username)


class Excelpost(db.Model):
    __tablename__ = 'excels'
    id = db.Column(db.Integer, primary_key=True)
    subcounty = db.Column(db.String(255),index=True,unique=True)
    parish = db.Column(db.String(255),index=True,unique=True)
    village = db.Column(db.String(255),index=True)


class Import( db.Model):
	__tablename__ = 'import'
	id = db.Column(db.Integer, primary_key=True)
	importname = db.Column(db.String(255),index=True)

class LC5(db.Model):
	__tablename__ = 'lc5'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)


class WomanMP(db.Model):
	__tablename__ = 'womanmp'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)


class WomanCounsellor(db.Model):
	__tablename__ = 'womanc'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)

class NRM(db.Model):
	__tablename__ = 'nrm_mps'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)

class Special(db.Model):
	__tablename__ = 'special_gps'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)

class ER(db.Model):
	__tablename__ = 'er_mps'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)

class ARMY(db.Model):
	__tablename__ = 'army_mps'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)

class Constituency(db.Model):
	__tablename__ = 'constituency_leaders'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)

class League(db.Model):
	__tablename__ = 'league_leaders'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)

class Other(db.Model):
	__tablename__ = 'other_leaders'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), index=True)
	name = db.Column(db.String(255),index=True)
	email = db.Column(db.String(255),index=True,unique=True)
	position = db.Column(db.String(255),index=True)
	year = db.Column(db.Date,index=True)
	contact = db.Column(db.String(255),index=True,unique=True)


