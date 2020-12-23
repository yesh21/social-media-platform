from flask import render_template, flash, redirect, url_for, session, request, make_response
from app import app
from .forms import LoginForm, SignupForm
from app import db, models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
            else:
                flash("incorrect password")

        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
        else:
            flash("email id not exists")
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = models.User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

    return render_template('signup.html', form=form)

@app.route('/home')
@login_required
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'])
    userqr = qrcodes.query.filter_by(user = current_user).all()
    user = current_user.username
    return render_template("base.html",user_image = full_filename,todo_list=userqr,title=user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))