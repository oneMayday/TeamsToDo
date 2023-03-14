from django.db import models

from users.models import User


class Task(models.Model):
	"""Task model"""
	title = models.CharField('Название задачи', max_length=100)
	description = models.CharField('Описание задачи', max_length=255, null=True)
	status = models.BooleanField('Статус задачи', default=False)
	create_date = models.DateField('Дата создания', auto_now_add=True)
	due_date = models.DateField('Дата окончания', null=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Задача'
		verbose_name_plural = 'Задачи'

	def __str__(self):
		return self.title


class PersonalList(models.Model):
	"""Personal user's tasks list"""
	title = models.CharField('Название', max_length=100)
	description = models.CharField('Описание', max_length=255, null=True)
	tasks = models.ManyToManyField(Task)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	time_create = models.TimeField('Время создания', auto_now_add=True)
	date_create = models.DateField('Дата создания', auto_now_add=True)

	class Meta:
		verbose_name = 'Личный список'
		verbose_name_plural = 'Личные списки'

	def __str__(self):
		return self.title


class TeamList(models.Model):
	"""List of tasks for the team work"""
	title = models.CharField('Название', max_length=100)
	description = models.CharField('Описание', max_length=255, null=True)
	tasks = models.ManyToManyField(Task)
	members = models.ManyToManyField(User)
	time_create = models.TimeField('Время создания', auto_now_add=True)
	date_create = models.DateField('Дата создания', auto_now_add=True)

	class Meta:
		verbose_name = 'Командный список'
		verbose_name_plural = 'Командные списки'

	def __str__(self):
		return self.title
