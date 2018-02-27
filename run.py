from flask import *
from forms import *
from models import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from werkzeug import secure_filename
import xlrd


app = Flask(__name__, instance_relative_config=True)
WTF_CSRF_ENABLED = True
app.secret_key = "national resistance movement"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dengima@localhost/logbook'
app.config['SQLALCHEMY_ECHO'] = True  # Show SQL commands created
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['ALLOWED_EXTENSIONS'] = set(['xls', 'xlsx', 'ods', 'csv', 'tsv', 'csvz', 'tsvz'])
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024 
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') +'/static/uploads/doc'
UPLOAD_FOLDER1 =  'static/files'
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1


db=SQLAlchemy(app)
login_manager =  LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/index'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.filter(Admin.id == int(admin_id)).first()


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None:
            if (user.role == 'normal_user'):
                if sha256_crypt.verify(form.password.data,user.password):
                    user.authenticated = True
                    login_user(user)
                    flash('You are now logged in', 'success')
                    return redirect(url_for('home_page'))
                else:
                    flash("Wrong Password, Try again", 'danger')
                    return redirect(url_for('index'))
        if admin is not None:
            if (admin.role == 'admin_user'):
                if sha256_crypt.verify(form.password.data,admin.password):
                    admin.authenticated = True
                    login_user(admin)
                    flash('You are now logged in', 'success')
                    return redirect(url_for('chairman'))
                else:
                    flash("Wrong Password, Try again", 'danger')
                    return redirect(url_for('index'))

        else:
            flash("Username not found, enter correcct username",'danger')
            return redirect(url_for('index'))

    return render_template("index.html", form=form)


@app.route("/chairman")
@login_required
def chairman():

    people = Excelpost.query.all()
    lc5 = LC5.query.all()
    wmp = WomanMP.query.all()
    wmc = WomanCounsellor.query.all()
    nrm = NRM.query.all()
    special = Special.query.all()
    er = ER.query.all()
    army = ARMY.query.all()
    const = Constituency.query.all()
    league = League.query.all()
    other = Other.query.all()

    return render_template("chairman.html", people=people,lc5=lc5,wmp=wmp,wmc=wmc,nrm=nrm,special=special,
                            er=er,army=army,const=const,league=league,other=other)


@app.route("/dashboard", methods=['POST','GET'])
@login_required
def dashboard():

    form = ImportForm(request.form)
    if request.method == 'POST' and form.validate():
        exceldoc = request.files['importname']
        filename = ' ';
        if exceldoc and allowed_file(exceldoc.filename):
            filename = secure_filename(exceldoc.filename)
            exceldoc.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Please upload the files with the extentions below !!!','danger')
            return redirect(url_for("dashboard"))
        imp = Import(importname = exceldoc )
        db.session.add(imp)
        db.session.commit()
        return redirect(url_for('chairman', filename=filename))
    return render_template("dashboard.html",form=form)


@app.route("/home_page")
@login_required
def home_page():

    people = Excelpost.query.all()
    lc5 = LC5.query.all()
    wmp = WomanMP.query.all()
    wmc = WomanCounsellor.query.all()
    nrm = NRM.query.all()
    special = Special.query.all()
    er = ER.query.all()
    army = ARMY.query.all()
    const = Constituency.query.all()
    league = League.query.all()
    other = Other.query.all()

    return render_template("home_page.html", people=people,lc5=lc5,wmp=wmp,wmc=wmc,nrm=nrm,special=special,
                            er=er,army=army,const=const,league=league,other=other)

@app.route('/upload', methods=['POST','GET'])
@login_required
def upload():

    form = UploadForm()
    if form.validate_on_submit():
        option = form.category.data
        
        if (option == 'lc5_chairperson'):
            new_lc5 = LC5(name=form.name.data,email=form.email.data,position=form.position.data,
                                year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_lc5)
            db.session.commit()
            flash('LC5 chairman uploaded successfully','success')
            return redirect(url_for('chairman'))

        elif (option == 'woman_mp'):
            new_womanmp = WomanMP(name=form.name.data,email=form.email.data,position=form.position.data,
                            year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_womanmp)
            db.session.commit()
            flash('Woman MP uploaded successfully','success')
            return redirect(url_for('chairman'))

        elif (option == 'woman_counsellor'):
            new_womanc = WomanCounsellor(name=form.name.data,email=form.email.data,position=form.position.data,
                            year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_womanc)
            db.session.commit()
            flash('Woman Counsellor uploaded successfully','success')
            return redirect(url_for('chairman'))

        elif (option == 'nrm_mp'):
            new_nrm = NRM(name=form.name.data,email=form.email.data,position=form.position.data,
                            year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_nrm)
            db.session.commit()
            flash('NRM Chairperson uploaded successfully','success')
            return redirect(url_for('chairman'))

        elif (option == 'special_gps'):
            new_special = Special(name=form.name.data,email=form.email.data,position=form.position.data,
                            year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_special)
            db.session.commit()
            flash('Special GPs uploaded successfully','success')
            return redirect(url_for('chairman'))
        elif (option == 'er_mp'):
            new_er = ER(name=form.name.data,email=form.email.data,position=form.position.data,
                            year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_er)
            db.session.commit()
            flash('ER MPs uploaded successfully','success')
            return redirect(url_for('chairman'))

        elif (option == 'army_mp'):
            new_army = ARMY(name=form.name.data,email=form.email.data,position=form.position.data,
                            year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_army)
            db.session.commit()
            flash('ARMY MP uploaded successfully','success')
            return redirect(url_for('chairman'))

        elif (option == 'constituency_leader'):
            new_const = Constituency(name=form.name.data,email=form.email.data,position=form.position.data,
                            year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_const)
            db.session.commit()
            flash('Constituency Leader uploaded successfully','success')
            return redirect(url_for('chairman'))

        elif (option == 'league_leader'):
            new_ledge = League(name=form.name.data,email=form.email.data,position=form.position.data,
                            year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_ledge)
            db.session.commit()
            flash('League leader uploaded successfully','success')
            return redirect(url_for('chairman'))

        elif (option == 'other_leader'):
            new_other = Other(name=form.name.data,email=form.email.data,position=form.position.data,
                            year=form.year.data,contact=form.contact.data,category=form.category.data)
            db.session.add(new_other)
            db.session.commit()
            flash('Leader uploaded successfully','success')
            return redirect(url_for('chairman'))
        else:
            flash('please a select a catergory', 'warning')
            return redirect(url_for('upload'))

    return render_template('upload.html',form=form)


@app.route('/register', methods=['POST','GET'])
@login_required
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        rol = form.role.data
        if (rol == 'normal_user'):
            new_user = User(username=form.username.data, email=form.email.data, role=form.role.data, password=sha256_crypt.encrypt(str(form.password.data)))
            db.session.add(new_user)
            db.session.commit()
            flash('New user added successfully','success')
            return redirect(url_for('chairman'))
        if (rol == 'admin_user'):
            admin = Admin(username=form.username.data, email=form.email.data, role=form.role.data, password=sha256_crypt.encrypt(str(form.password.data)))
            db.session.add(admin)
            db.session.commit()
            flash('Admin user added successfully','success')
            return redirect(url_for('chairman'))
    return render_template('register.html', form=form)


@app.route("/delete/<int:id>" ,methods=['POST'])
@login_required
def delete(id):
    remove = Excelpost.query.get_or_404(id)
    db.session.delete(remove)
    db.session.commit()
    flash("Deleted successfully", 'danger')
    return redirect(url_for('chairman'))
    return render_template('chairman.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out now','warning')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

