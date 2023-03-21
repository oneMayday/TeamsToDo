from django.db import models

from users.models import User


class TeamList(models.Model):
	"""List of tasks for the team work"""
	title = models.CharField('Название', max_length=100)
	description = models.CharField('Описание', max_length=255, null=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
	members = models.ManyToManyField(User, related_name='members')
	time_create = models.TimeField('Время создания', auto_now_add=True)
	date_create = models.DateField('Дата создания', auto_now_add=True)

	class Meta:
		verbose_name = 'Командный список'
		verbose_name_plural = 'Командные списки'

	def __str__(self):
		return self.title

	def __repr__(self):
		return self.title


class Task(models.Model):
	"""Task model"""
	title = models.CharField('Описание задачи', max_length=200)
	status = models.BooleanField('Статус задачи', default=False)
	create_date = models.DateField('Дата создания', auto_now_add=True)
	update_date = models.DateField('Дата обновления', auto_now_add=True)
	due_date = models.DateField('Дата окончания', null=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	teamlist_relation = models.ForeignKey(
		TeamList,
		on_delete=models.CASCADE,
		related_name='tasks',
		verbose_name='Добавить в список:'
	)

	class Meta:
		verbose_name = 'Задача'
		verbose_name_plural = 'Задачи'

	def __str__(self):
		return f'{self.pk}: {self.title}'

	def __repr__(self):
		return self.title
