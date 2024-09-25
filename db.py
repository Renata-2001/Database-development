import psycopg2
import click

import psycopg2.extras

class DanceDB:
	def __init__(self, config):
		self.config = config
		self.conn = psycopg2.connect(
      		dbname=self.config['DATABASE'], user=self.config['USERNAME'],
      		password=self.config['PASSWORD'], host=self.config['HOST'],
      		cursor_factory=psycopg2.extras.DictCursor
    	)
		with self.conn:
				with self.conn.cursor() as cur:
					cur.execute("SET TIMEZONE TO 'UTC'")


	def __del__(self):
		self.conn.close()

#------------ADD_RECORDS_TO_TABLES-----------------------
	def add_user(self, login, hash, email):   #USERS
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('INSERT INTO users (login, passwd, email) VALUES (%s, %s, %s);', (login, hash, email))

		
	def add_styles(self, style):  #STYLES
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('INSERT INTO styles (style) VALUES (%s);', (style,))


	def add_public(self, user_id, video_path, description = None, style_id = None):  #PUBLICATIONS
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('INSERT INTO publications (user_id, description, video_path, style_id) VALUES (%s, %s, %s, %s);', (user_id, description, video_path, style_id))


	def add_comment(self, user_id, public_id, comment_text):  #COMMENT_PUBLIC
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('INSERT INTO comment_public (user_id, public_id, comment_text) VALUES (%s, %s, %s);', (user_id, public_id, comment_text))


	def add_like(self, user_id, public_id):  #SAVED_PUBLIC
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('INSERT INTO likes_public (user_id, public_id) VALUES (%s, %s);', (user_id, public_id))


	def add_follower(self, user_id, follower_id):   #FOLLOWERS
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('INSERT INTO followers (user_id, follower_id) VALUES (%s, %s);', (user_id, follower_id))


#------------UPDATE_RECORDS_IN_TABLES-----------------------
	def update_user(self, user_id, login=None, hash=None, email=None):   #USERS
		with self.conn:
			with self.conn.cursor() as cur:
				if login is not None:
					cur.execute('UPDATE users SET login = %s WHERE user_id = %s;', (login, user_id))
				if hash is not None:
					cur.execute('UPDATE users SET passwd = %s WHERE user_id = %s;', (hash, user_id))
				if email is not None:
					cur.execute('UPDATE users SET email = %s WHERE user_id = %s;', (email, user_id))
				

	def update_public(self, public_id, description = None, style_id = None):  #PUBLICATIONS
		with self.conn:
			with self.conn.cursor() as cur:
				if description is not None:
					cur.execute('UPDATE publications SET description = %s WHERE public_id = %s;', (description, public_id))
				if style_id is not None:
					cur.execute('UPDATE publications SET passwd = %s WHERE public_id = %s;', (style_id, public_id))


	def update_comment(self, user_id, public_id, comment_text):  #COMMENT_PUBLIC
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('UPDATE comment_public SET comment_text = %s WHERE user_id = %s AND public_id = %s;', (comment_text, user_id, public_id))
				
#------------DELETE_RECORDS_FROM_TABLE-------------

	def delete_public(self, public_id):  #PUBLICATIONS
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('DELETE FROM publications WHERE public_id = %s;',(public_id))


	def delete_comment(self, user_id, public_id):  #COMMENT_PUBLIC
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('DELETE FROM comment_public WHERE public_id = %s AND user_id = %s;',(public_id, user_id))


	def delete_like(self, user_id, public_id):  #SAVED_PUBLIC
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('DELETE FROM likes_public WHERE public_id = %s AND user_id = %s;',(public_id, user_id))
	

	def delete_follower(self, user_id, follower_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('DELETE FROM followers WHERE follower_id = %s AND user_id = %s;',(follower_id, user_id))


#------------SELECT_RECORDS_FROM_TABLE-------------
	def get_user_by_login(self, login):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT * FROM users WHERE login = %s LIMIT 1', (login,))
				user = cur.fetchone()
		return user
	
	def get_user_id_by_login(self, login):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT user_id FROM users WHERE login = %s LIMIT 1', (login,))
				user = cur.fetchone()
		return user
		
	def get_subscriptions(self, user_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT login FROM followers JOIN users on followers.follower_id = users.user_id WHERE followers.user_id = %s', (user_id,))
				subscriptions = [ data['login'] for data in cur.fetchall()]
		return subscriptions
	
	def get_follower(self, user_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT login FROM followers JOIN users on followers.user_id = users.user_id WHERE followers.follower_id = %s', (user_id,))
				follower = [ data['login'] for data in cur.fetchall()]
		return follower
	
	def get_likes(self, user_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT publications.public_id as public_id, publications.video_path as video_path FROM publications JOIN likes_public on likes_public.public_id = publications.public_id WHERE likes_public.user_id = %s', (user_id,))
				publics = cur.fetchall()
		return publics

	def is_free_login(self, login):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT count(*) as cnt FROM users WHERE login = %s', (login,))
				amount = cur.fetchone()
				if amount[0] == 0:
					return True
				else:
					return False
		

	def get_user(self, user_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT * FROM users WHERE user_id = %s LIMIT 1', (user_id,))
				user = cur.fetchone()
				if not user:
					return False
				return user

		
	def get_style_id(self, style):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT * FROM styles WHERE style = %s LIMIT 1', (style,))
				style = cur.fetchone()
		return style


	def get_public_by_id(self, public_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT * FROM publications WHERE public_id = %s LIMIT 1', (public_id,))
				public = cur.fetchone()
		return public
	

	def get_users_logins(self):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT login FROM users')
				logins = [ data['login'] for data in cur.fetchall()]
		return logins
		
		
	def get_all_styles(self):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT * FROM styles')
				styles = cur.fetchall()
		return styles
		
	def get_all_publics(self):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT video_path FROM publications')
				publics = cur.fetchone()
		return publics

		
	def get_video_by_user_id(self, user_id):
		with self.conn:
			with self.conn.cursor() as cur:
					cur.execute('SELECT * FROM publications WHERE user_id = %s', (user_id,))
					publics = cur.fetchall()
		return publics
		

	def check_follow(self, user_id, follower_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT * FROM followers WHERE user_id = %s and follower_id = %s', (user_id, follower_id, ))
				check =  cur.fetchall() 
		return check
	
	def check_like(self, user_id, public_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT * FROM likes_public WHERE user_id = %s and public_id = %s', (user_id, public_id, ))
				check =  cur.fetchall() 
		return check
	
	def likes_of_the_public(self, public_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT login FROM publications join users on users.user_id=publications.user_id WHERE public_id = %s', (public_id, ))
				login = [ data['login'] for data in cur.fetchall()]
		return login
	

	def get_comments(self, public_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT users.login as login, comment_public.comment_text as text, comment_public.public_id as public_id, comment_public.user_id as user_id FROM comment_public join users on users.user_id=comment_public.user_id WHERE comment_public.public_id = %s', (public_id, ))
				comments = cur.fetchall()
		return comments

	def count_likes(self, public_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT COUNT(user_id) as count_of_likes FROM publications WHERE public_id = %s', (public_id, ))
				count =  cur.fetchall() 
		return count
	
	def get_public_by_style_id(self, style_id):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute('SELECT * FROM publications WHERE style_id = %s', (style_id, ))
				styles =  cur.fetchall() 
		return styles