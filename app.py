import os
import json
import uuid

import psycopg2 
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask import Flask, redirect, url_for, render_template, request, session, g, current_app, flash
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash, check_password_hash

from db import DanceDB
from login import UserLogin

app = Flask(__name__)

login_manager = LoginManager(app)

@app.route('/')
def index():
	return render_template('main.html',
			loggedin=current_user,
			values=dancedb.get_all_styles()
	)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = dancedb.get_user_by_login(request.form['login'])
		if user and check_password_hash(user['passwd'], request.form['passwd']):
			userLogin = UserLogin().create(user)
			login_user(userLogin)
			return redirect(url_for('index'))
	return render_template('login.html',
			loggedin=current_user
	)

@app.route('/profile')
@login_required
def profile():
	user_id = int(current_user.get_id())
	videos = dancedb.get_video_by_user_id(user_id)
	return render_template('profile.html',
		user_id=current_user.get_id() if current_user else None,
		loggedin=current_user,
		videos=videos
	)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if len(request.form['login']) >= 0 and len(request.form['passwd1']) >= 0 and (request.form['passwd1'] == request.form['passwd2']):
			if dancedb.is_free_login(request.form['login']):	
				print('reg new user\n')				
				hash = generate_password_hash(request.form['passwd1'])
				dancedb.add_user(request.form['login'], hash, request.form['email'])
				return redirect(url_for('login'))
	return render_template('register.html',
			loggedin=current_user
	)


@login_manager.user_loader
def load_user(user_id):
	print('load user')
	print(user_id)
	return UserLogin().fromDB(user_id, dancedb)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
	if request.method == 'POST':	
		dancedb.add_styles(request.form['style'])
		style_id = dancedb.get_style_id(request.form['style'])	
		user_id = int(current_user.get_id())
		for f in request.files.getlist('video'):
			if f.filename == '':
				continue
			name = get_free_name()
			_, ext = os.path.splitext(f.filename)
			if ext in ['.avi', '.mkv', '.mp4', '.ogg']:
				f.save(os.path.join('video', name + ext))
				dancedb.add_public(user_id, name + ext, request.form['description'] , style_id)
			else:
				flash('Неправильный формат видео')
				print('Wrong video format')
				return redirect(url_for('profile'))
		return redirect(url_for('profile'))
	return render_template('upload.html',
			loggedin=current_user)

dancedb = None
@app.before_request
def before_request():
	global dancedb
	db = get_db()
	dancedb = DanceDB(db)

@app.teardown_appcontext
def close_db(error=None):
	if hasattr(g, 'db'):
		g.db.close()

def get_db():
	if not hasattr(g, 'db'):
		g.db = psycopg2.connect(dbname= 'dancedb', user='renatik', password = 'Bizezo_00')
	return g.db

def get_free_name():
	name = str(uuid.uuid4())
	pathname = os.path.join('video', name)
	while os.path.exists(pathname):
		name = str(uuid.uuid4())
		pathname = os.path.join('video', name)
	return name


if __name__ == '__main__':
   app.secret_key = os.urandom(24)
   app.run(debug=True, host='0.0.0.0', port='8000')