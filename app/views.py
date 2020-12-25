from flask import render_template, flash, redirect, url_for, session, request, make_response
from app import app
from .forms import LoginForm, SignupForm,PostForm
from app import db, models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


db.create_all()
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

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
                session['email'] = user.email
                login_user(user, remember=form.remember.data)
                flash('Logged in successfully.')
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
        new_user = models.User(username=form.username.data, email=form.email.data, password=hashed_password,lastname=form.lastname.data,firstname = form.firstname.data)
        db.session.add(new_user)
        db.session.commit()
        flash("new account created")
        return render_template('login.html', form=form)

    return render_template('signup.html', form=form)

@app.route('/home')
@login_required
def home():
    return 'done successfully'

@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():

	form = PostForm()
	if form.validate_on_submit():
		post = models.Post(title=form.title.data, user=current_user.userid, message=form.message.data)
		db.session.add(post)
		db.session.commit()

		flash("new post created")

		return redirect( url_for( 'home' ) )

	return render_template('newpost.html',
						   title='New Post',
						   form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("logout sucessfully")
    return redirect(url_for('login'))