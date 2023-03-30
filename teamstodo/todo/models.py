from django.db import models

from users.models import User


class TeamList(models.Model):
	"""List of tasks for the team work."""
	title = models.CharField('Название', max_length=100)
	description = models.CharField('Описание', max_length=255, null=True)
	time_create = models.TimeField('Время создания', auto_now_add=True)
	date_create = models.DateField('Дата создания', auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_owner')
	members = models.ManyToManyField(User, related_name='members')

	class Meta:
		verbose_name = 'Командный список'
		verbose_name_plural = 'Командные списки'
		ordering = ['title']

	def __str__(self):
		return self.title

	def __repr__(self):
		return self.title


class Task(models.Model):
	"""Task model."""
	title = models.CharField('Описание задачи', max_length=200)
	status = models.BooleanField('Статус задачи', default=False)
	create_date = models.DateField('Дата создания', auto_now_add=True)
	update_date = models.DateField('Дата обновления', auto_now_add=True)
	due_date = models.DateField('Дата окончания', null=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_owner')
	who_takes = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='who_takes',
		verbose_name='Исполнитель'
	)
	teamlist_relation = models.ForeignKey(
		TeamList,
		on_delete=models.CASCADE,
		related_name='tasks',
		verbose_name='Добавить в список:'
	)

	class Meta:
		verbose_name = 'Задача'
		verbose_name_plural = 'Задачи'
		ordering = ['teamlist_relation']

	def __str__(self):
		string = f'{self.pk}. {self.title}. Статус: {self.status}. Исполнитель: {self.who_takes}'
		return string

	def __repr__(self):
		return self.title
