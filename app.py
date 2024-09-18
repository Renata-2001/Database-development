import os
import json
import uuid

import psycopg2 
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask import Flask, redirect, url_for, render_template, request, session, g, current_app, flash, Config
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash, check_password_hash

from db import DanceDB
from login import UserLogin

app = Flask(__name__)

cfg = Config(os.path.dirname(__file__))
cfg.from_envvar('CONFIG')

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
	login = dancedb.get_user(user_id)['login']
	filename = dancedb.get_video_by_user_id(user_id)
	media_path = cfg['MEDIA_PATH']
	videos = []
	for v in filename:
		_, ext = os.path.splitext(v)
		print(ext)
		videos.append({'path': os.path.join(media_path, v), 'ext': ext[1:]})
	return render_template('profile.html',
		user_id=current_user.get_id() if current_user else None,
		loggedin=current_user,
		videos=videos,
		login=login
	)

@app.route('/profile_id/<login>', methods=['GET'])
@login_required
def profile_id(login):
	user_id = dancedb.get_user_by_login(login)['user_id']
	if dancedb.check_follow(current_user.get_id(), user_id):
		what = "Отписаться"
	else:
		what = "Подписаться"
	filename = dancedb.get_video_by_user_id(user_id)
	media_path = cfg['MEDIA_PATH']
	videos = []
	for v in filename:
		_, ext = os.path.splitext(v)
		videos.append({'path': os.path.join(media_path, v), 'ext': ext[1:]})
	return render_template('profile_id.html',
		loggedin=current_user,
		login = login,
		videos = videos,
		what = what
	)

@app.route('/follow/<login>', methods=['GET'])
@login_required
def follow(login):
	user_id = dancedb.get_user_by_login(login)['user_id']
	if user_id == current_user.get_id():
		flash('You cannot follow yourself!')
		return redirect(url_for('profile_id'))
	if dancedb.check_follow(current_user.get_id(), user_id):
		dancedb.delete_follower(current_user.get_id(), user_id)
		flash(f'You are unfollowing {login}!')
		return redirect(url_for('followers'))
	else:
		dancedb.add_follower(current_user.get_id(), user_id)
		flash(f'You are following {login}!')
		return redirect(url_for('subscriptions'))


@app.route('/profile/followers/<login>', methods=['GET'])
@login_required
def followers(login):
	user_id = dancedb.get_user_by_login(login)['user_id']
	users = dancedb.get_follower(user_id)
	return render_template('users.html',
		loggedin=current_user,
		users=users,
		who = 'Подписчики'
	)

@app.route('/profile/subscriptions/<login>', methods=['GET'])
@login_required
def subscriptions(login):
	user_id = dancedb.get_user_by_login(login)['user_id']
	users = dancedb.get_subscriptions(user_id)
	return render_template('users.html',
		loggedin=current_user,
		users=users,
		who = 'Подписки'
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
				print('printreg new user\n')				
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
		user_id = int(current_user.get_id())
		for f in request.files.getlist('video'):
			if f.filename == '':
				continue
			name = get_free_name()
			_, ext = os.path.splitext(f.filename)
			if ext in ['.avi', '.mkv', '.mp4', '.ogg']:
				f.save(os.path.join(cfg['MEDIA_PATH'], name + ext))
				dancedb.add_public(user_id, name + ext, request.form['description'], request.form['style'])
			else:
				flash('Неправильный формат видео')
				print('Wrong video format')
				return redirect(url_for('profile'))
	return render_template('upload.html',
			loggedin=current_user,
			styles=dancedb.get_all_styles()
			)

@app.route('/add_style', methods=['GET', 'POST'])
@login_required
def add_style():
	if request.method == 'POST':	
		dancedb.add_styles(request.form['style'])	
		return redirect(url_for('upload'))
	return render_template('upload.html',
			loggedin=current_user,
			styles=dancedb.get_all_styles()
			)

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
		g.db = psycopg2.connect(dbname=cfg['DATABASE'], user=cfg['USERNAME'], password = cfg['PASSWORD'])
	return g.db

def get_free_name():
	name = str(uuid.uuid4())
	pathname = os.path.join(cfg['MEDIA_PATH'] , name)
	while os.path.exists(pathname):
		name = str(uuid.uuid4())
		pathname = os.path.join(cfg['MEDIA_PATH'] , name)
	return name


if __name__ == '__main__':
   app.secret_key = cfg['SECRET_KEY']
   app.run(debug=True, host='0.0.0.0', port='8000')