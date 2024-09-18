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


@app.route('/profile')   #работа со своим профилем
@login_required
def profile():
	user_id = int(current_user.get_id())
	login = dancedb.get_user(user_id)['login']
	public = dancedb.get_video_by_user_id(user_id)
	media_path = cfg['MEDIA_PATH']
	videos = []
	for v in public:
		_, ext = os.path.splitext(v['video_path'])
		videos.append({'path': os.path.join(media_path, v['video_path']), 'ext': ext[1:], 'public_id': v['public_id']})
	return render_template('profile.html',
		user_id=current_user.get_id() if current_user else None,
		loggedin=current_user,
		videos=videos,
		login=login
	)


@app.route('/profile_id/<login>', methods=['GET'])   #просмотр чужого профиля
@login_required
def profile_id(login):
	if login == dancedb.get_user(current_user.get_id())['login']:
		return redirect(url_for('profile'))
	else:
		user_id = dancedb.get_user_by_login(login)['user_id']
		if dancedb.check_follow(current_user.get_id(), user_id):
			what = "Отписаться"
		else:
			what = "Подписаться"
		public = dancedb.get_video_by_user_id(user_id)
		media_path = cfg['MEDIA_PATH']
		videos = []
		for v in public:
			_, ext = os.path.splitext(v)
			videos.append({'path': os.path.join(media_path, v), 'ext': ext[1:], 'public_id': v['public_id']})
		return render_template('profile_id.html',
			loggedin=current_user,
			login = login,
			videos = videos,
			what = what
		)


@app.route('/profile/likes')   # просмотр понравивишихся публикаций
@login_required
def likes():
	user_id = current_user.get_id()
	publics= dancedb.get_likes(user_id)
	media_path = cfg['MEDIA_PATH']
	videos = []
	for v in publics:
		_, ext = os.path.splitext(v['video_path'])
		videos.append({'path': os.path.join(media_path, v['video_path']), 'ext': ext[1:], 'public_id': v['public_id']})
	return render_template('publics.html',
		loggedin=current_user,
		videos=videos,
		what = 'Любимое'
	)

@app.route('/follow/<login>', methods=['GET'])   # подписка и отписка от чужого аккаунта
@login_required
def follow(login):
	user_id = dancedb.get_user_by_login(login)['user_id']
	if user_id == current_user.get_id():
		flash('You cannot follow yourself!')
		return redirect(url_for('profile_id'))
	if dancedb.check_follow(current_user.get_id(), user_id):
		dancedb.delete_follower(current_user.get_id(), user_id)
		flash(f'You are unfollowing {login}!')
		return redirect(url_for('followers', login=dancedb.get_user(current_user.get_id())['login']))
	else:
		dancedb.add_follower(current_user.get_id(), user_id)
		flash(f'You are following {login}!')
		return redirect(url_for('subscriptions', login=dancedb.get_user(current_user.get_id())['login']))


@app.route('/profile/followers/<login>', methods=['GET'])  # просмотр подписчиков
@login_required
def followers(login):
	user_id = dancedb.get_user_by_login(login)['user_id']
	users = dancedb.get_follower(user_id)
	return render_template('users.html',
		loggedin=current_user,
		users=users,
		who = 'Подписчики'
	)

@app.route('/profile/subscriptions/<login>', methods=['GET'])   # просмотр подписок
@login_required
def subscriptions(login):
	user_id = dancedb.get_user_by_login(login)['user_id']
	users = dancedb.get_subscriptions(user_id)
	return render_template('users.html',
		loggedin=current_user,
		users=users,
		who = 'Подписки'
	)

@app.route('/<public_id>', methods=['GET'])  #просмотр публикации "подробнее" - здесь можно писать комментарии и добавлять в любимое
@login_required
def public(public_id):
	public = dancedb.get_public_by_id(public_id)
	comments = dancedb.get_comments(public_id)
	if dancedb.check_like(current_user.get_id(), public_id):
		what = "Удалить из избранного"
	else:
		what = "Добавить в избранное"
	media_path = cfg['MEDIA_PATH']
	_, ext = os.path.splitext(public['video_path'])
	video = ({'path': os.path.join(media_path, public['video_path']), 'ext': ext[1:]})
	return render_template('public.html',
			loggedin=current_user,
			what=what,
			video=video,
			public_id=public_id,
			description = public['description'],
			count = dancedb.count_likes(public_id),
			comments=comments
	)


@app.route('/<public_id>/like', methods=['GET'])  #публикацию можно лайкнуть
@login_required
def like(public_id):
	if dancedb.check_like(current_user.get_id(), public_id):
		dancedb.delete_like(current_user.get_id(), public_id)
		return redirect(url_for('public', public_id=public_id))
	else:
		dancedb.add_like(current_user.get_id(), public_id)
		return redirect(url_for('public', public_id=public_id))
	

@app.route('/<public_id>/likes', methods=['GET'])  # просмотр лайков
@login_required
def likes_of_the_public(public_id):
	users = dancedb.likes_of_the_public(public_id)
	return render_template('users.html',
		loggedin=current_user,
		users=users,
		who = 'Этим людям понравилась публикация'
	)
	

@app.route('/<public_id>/add_comment', methods=['GET', 'POST'])  #публикацию можно прокомментировать
@login_required
def add_comment(public_id):
	if request.method == 'POST':	
		print('this', request.form['comment'])
		dancedb.add_comment(int(current_user.get_id()), public_id, request.form['comment'])	
		return redirect(url_for('public', public_id = public_id))
	return 'hello'





@login_manager.user_loader
def load_user(user_id):
	print('load user')
	print(user_id)
	return UserLogin().fromDB(user_id, dancedb)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
	if request.method == 'POST':	
		print(request.form['style'], '----style')
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