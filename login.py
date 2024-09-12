class UserLogin:
	def fromDB(self, user_id, dancedb):
		self.__user = dancedb.get_user(user_id)
		return self

	def create(self, user):
		self.__user = user
		return self

	def is_authenticated(self):
		if self.__user:
			return True
		else:
			return False

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.__user['user_id'])

	def get_login(self):
		return str(self.__user['login'])