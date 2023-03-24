from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	"""Custom user class."""
	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return self.username

	def __repr__(self):
		return self.username
