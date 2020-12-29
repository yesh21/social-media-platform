from flask import render_template, flash, redirect, url_for, session, request, make_response, jsonify
from app import app
from .forms import LoginForm, SignupForm,PostForm
from app import db, models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc
from datetime import datetime


app.config["IMAGE_UPLOADS"] = "app/static/Image_UPLOADS/uploads/"
app.config["IMAGE_UPLOADS1"] = "app/static/Image_UPLOADS/profiles/"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

severityList = ['TEST', 'WARNING', 'UPDATE', 'SEVERE']
def appLog( severe, log ):
	file = open("log.txt", "a")
	file.write("{1} -- {0} | {2}\n".format(severityList[severe], datetime.now().strftime("%Y-%m-%d %H:%M"), log))
	file.close()

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
                appLog(1, "{0} has logged".format(user.email))
                return redirect(url_for('home'))
            else:
                appLog(3, "{0} tried loggin' w/ incorrect password".format(user.email))
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
    return render_template('home.html')

@app.route('/profile')
@login_required
def profile():
    userposts = models.Post.query.filter_by(user = current_user.userid).all()
    allusers = models.User.query.filter_by().all()
    followers = []
    following = []
    for users in allusers:
     userfollowers = users.is_following(current_user)
     userfollowing = current_user.is_following(users)
     if userfollowers > 0:
         followers.append( users.username)
     if userfollowing > 0:
         following.append( users.username)


    return render_template('profile.html',userposts = userposts,userfollowers=followers, userfollowing= following)

@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():

	form = PostForm()
	if form.validate_on_submit():
		post = models.Post(title=form.title.data, user=current_user.userid, message=form.message.data)
		db.session.add(post)
		db.session.commit()
		userposts = models.Post.query.order_by(desc(models.Post.date)).first()
		file = request.files['image']
		if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['IMAGE_UPLOADS'], str(userposts.postid)+'.png')) 

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

@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
    if request.method == "POST":
        files = request.files['image']
        image = files.filename
        file = request.files['image']
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['IMAGE_UPLOADS1'], str(current_user.userid)+'.png')) 
                flash("new profile image uploaded")
                return render_template("home.html")
        else:
            return render_template("edit.html")
    else:
     return render_template("edit.html")

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = models.User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return render_template('home.html')
    if user == current_user:
        flash('You can\'t unfollow yourself!')
        return render_template('home.html')
    u = current_user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + username + '.')
        return render_template('home.html')
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + username + '.')
    appLog(2, "{0} has unfollowed ".format(current_user.email)+user.username )
    return render_template('home.html')

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = models.User.query.filter_by(username=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return render_template('home.html')
    if user == current_user:
        flash('You can\'t follow yourself!')
        return render_template('home.html')
    u = current_user.follow(user)
    if u is None:
        flash('already followed ' + nickname + '.')
        return render_template('home.html')
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    search = request.form.get("search")
    return redirect(url_for('search_results', query=search))

@app.route('/search_results/<query>')
def search_results(query):
    results1 = models.User.query.filter_by(username = query).all()
    results2 = models.User.query.filter_by(firstname = query).all()
    results3 = models.User.query.filter_by(lastname = query).all()
    results = results1 + results2 + results3
    return render_template('search_results.html',
                           query=query,
                           results=results)