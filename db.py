import psycopg2
import click

import psycopg2.extras


class DanceDB:
	def __init__(self, db):
		self.__db = db
		self.__cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

		
	def execute_script(self, script):
		self.__cursor.execute(script)
		self.__db.commit()

#------------ADD_RECORDS_TO_TABLES-----------------------
	def add_user(self, login, hash, email):   #USERS
		try:
			self.__cursor.execute('INSERT INTO users (login, passwd, email) VALUES (%s, %s, %s);', (login, hash, email))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)
		
	def add_styles(self, style):  #STYLES
		try:
			self.__cursor.execute('INSERT INTO styles (style) VALUES (%s);', (style,))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)

	def add_public(self, user_id, video_path, description = None, style_id = None):  #PUBLICATIONS
		try:
			self.__cursor.execute('INSERT INTO publications (user_id, description, video_path, style_id) VALUES (%s, %s, %s, %s);', (user_id, description, video_path, style_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)

	def add_comment(self, user_id, public_id, comment_text):  #COMMENT_PUBLIC
		try:
			self.__cursor.execute('INSERT INTO comment_public (user_id, public_id, comment_text) VALUES (%s, %s, %s);', (user_id, public_id, comment_text))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)

	def add_like(self, user_id, public_id):  #SAVED_PUBLIC
		try:
			self.__cursor.execute('INSERT INTO likes_public (user_id, public_id) VALUES (%s, %s);', (user_id, public_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)

	def add_follower(self, user_id, follower_id):   #FOLLOWERS
		try:
			self.__cursor.execute('INSERT INTO followers (user_id, follower_id) VALUES (%s, %s);', (user_id, follower_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)

#------------UPDATE_RECORDS_IN_TABLES-----------------------
	def update_user(self, user_id, login=None, hash=None, email=None):   #USERS
		if login is not None:
			try:
				self.__cursor.execute('UPDATE users SET login = %s WHERE user_id = %s;', (login, user_id))
				self.__db.commit()
			except psycopg2.Error as e:
				print(e.pgerror)
		if hash is not None:
			try:
				self.__cursor.execute('UPDATE users SET passwd = %s WHERE user_id = %s;', (hash, user_id))
				self.__db.commit()
			except psycopg2.Error as e:
				print(e.pgerror)
		if email is not None:
			try:
				self.__cursor.execute('UPDATE users SET email = %s WHERE user_id = %s;', (email, user_id))
				self.__db.commit()
			except psycopg2.Error as e:
				print(e.pgerror)

	def update_public(self, public_id, description = None, style_id = None):  #PUBLICATIONS
		if description is not None:
			try:
				self.__cursor.execute('UPDATE publications SET description = %s WHERE public_id = %s;', (description, public_id))
				self.__db.commit()
			except psycopg2.Error as e:
				print(e.pgerror)
		if style_id is not None:
			try:
				self.__cursor.execute('UPDATE publications SET passwd = %s WHERE public_id = %s;', (style_id, public_id))
				self.__db.commit()
			except psycopg2.Error as e:
				print(e.pgerror)

	def update_comment(self, user_id, public_id, comment_text):  #COMMENT_PUBLIC
		try:
			self.__cursor.execute('UPDATE comment_public SET comment_text = %s WHERE user_id = %s AND public_id = %s;', (comment_text, user_id, public_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)
#------------DELETE_RECORDS_FROM_TABLE-------------

	def delete_public(self, public_id):  #PUBLICATIONS
		try:
			self.__cursor.execute('DELETE FROM publications WHERE public_id = %s;',(public_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)

	def delete_comment(self, user_id, public_id):  #COMMENT_PUBLIC
		try:
			self.__cursor.execute('DELETE FROM comment_public WHERE public_id = %s AND user_id = %s;',(public_id, user_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)

	def delete_like(self, user_id, public_id):  #SAVED_PUBLIC
		try:
			self.__cursor.execute('DELETE FROM likes_public WHERE public_id = %s AND user_id = %s;',(public_id, user_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)

	def delete_follower(self, user_id, follower_id):
		try:
			self.__cursor.execute('DELETE FROM followers WHERE follower_id = %s AND user_id = %s;',(follower_id, user_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)


#------------SELECT_RECORDS_FROM_TABLE-------------
	def get_user_by_login(self, login):
		self.__cursor.execute('SELECT * FROM users WHERE login = %s LIMIT 1', (login,))
		user = self.__cursor.fetchone()
		return user
	
	def get_user_id_by_login(self, login):
		self.__cursor.execute('SELECT user_id FROM users WHERE login = %s LIMIT 1', (login,))
		user = self.__cursor.fetchone()
		return user
		
	def get_subscriptions(self, user_id):
		self.__cursor.execute('SELECT login FROM followers JOIN users on followers.follower_id = users.user_id WHERE followers.user_id = %s', (user_id,))
		subscriptions = [ data['login'] for data in self.__cursor.fetchall()]
		return subscriptions
	
	def get_follower(self, user_id):
		self.__cursor.execute('SELECT login FROM followers JOIN users on followers.user_id = users.user_id WHERE followers.follower_id = %s', (user_id,))
		follower = [ data['login'] for data in self.__cursor.fetchall()]
		return follower
	
	def get_likes(self, user_id):
		self.__cursor.execute('SELECT publications.public_id as public_id, publications.video_path as video_path FROM publications JOIN likes_public on likes_public.public_id = publications.public_id WHERE likes_public.user_id = %s', (user_id,))
		publics = self.__cursor.fetchall()
		return publics

	def is_free_login(self, login):
		try:
			self.__cursor.execute('SELECT count(*) as cnt FROM users WHERE login = %s', (login,))
			amount = self.__cursor.fetchone()
			print(amount)
			if amount[0] == 0:
				return True
			else:
				return False
		except psycopg2.Error as e:
			print(e.pgerror)
			return False
		

	def get_user(self, user_id):
		try:
			self.__cursor.execute('SELECT * FROM users WHERE user_id = %s LIMIT 1', (user_id,))
			user = self.__cursor.fetchone()
			if not user:
				return False
			return user
		except psycopg2.Error as e:
			print(e.pgerror)
			return False
		
	def get_style_id(self, style):
		try:
			self.__cursor.execute('SELECT * FROM styles WHERE style = %s LIMIT 1', (style,))
			user = self.__cursor.fetchone()
		except psycopg2.Error as e:
			print(e.pgerror)
			return False

	def get_public_by_id(self, public_id):
		self.__cursor.execute('SELECT * FROM publications WHERE public_id = %s LIMIT 1', (public_id,))
		public = self.__cursor.fetchone()
		return public

		

	def get_users_logins(self):
		try:
			self.__cursor.execute('SELECT login FROM users')
			logins = [ data['login'] for data in self.__cursor.fetchall()]
			return logins
		except psycopg2.Error as e:
			print(e.pgerror)
			return False
		
	def get_all_styles(self):
		self.__cursor.execute('SELECT * FROM styles')
		styles = self.__cursor.fetchall()
		return styles
		
	def get_all_publics(self):
		try:
			self.__cursor.execute('SELECT video_path FROM publications')
			publics = self.__cursor.fetchone()
			return publics
		except psycopg2.Error as e:
			print(e.pgerror)
			return False
		
	def get_video_by_user_id(self, user_id):
		try:
			self.__cursor.execute('SELECT * FROM publications WHERE user_id = %s', (user_id,))
			publics = self.__cursor.fetchall()
			return publics
		except psycopg2.Error as e:
			print(e.pgerror)
			return False

	def check_follow(self, user_id, follower_id):
		self.__cursor.execute('SELECT * FROM followers WHERE user_id = %s and follower_id = %s', (user_id, follower_id, ))
		check =  self.__cursor.fetchall() 
		return check
	
	def check_like(self, user_id, public_id):
		self.__cursor.execute('SELECT * FROM likes_public WHERE user_id = %s and public_id = %s', (user_id, public_id, ))
		check =  self.__cursor.fetchall() 
		return check
	
	def likes_of_the_public(self, public_id):
		self.__cursor.execute('SELECT login FROM publications join users on users.user_id=publications.user_id WHERE public_id = %s', (public_id, ))
		login = [ data['login'] for data in self.__cursor.fetchall()]
		return login
	

	def get_comments(self, public_id):
		self.__cursor.execute('SELECT users.login as login, comment_public.comment_text as text, comment_public.public_id as public_id, comment_public.user_id as user_id FROM comment_public join users on users.user_id=comment_public.user_id WHERE comment_public.public_id = %s', (public_id, ))
		comments = self.__cursor.fetchall()
		return comments

	def count_likes(self, public_id):
		self.__cursor.execute('SELECT COUNT(user_id) as count_of_likes FROM publications WHERE public_id = %s', (public_id, ))
		count =  self.__cursor.fetchall() 
		return count