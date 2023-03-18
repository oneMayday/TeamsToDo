import datetime

from django.test import TestCase
from django.test.client import Client

from todo.models import Task, PersonalList
from users.models import User


class Settings(TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()

		# Add users to db.
		cls.test_user1 = User.objects.create_user(
			username='test_user1',
			email='testuser1-email@test.ru',
			password='testuser1_password',
		)

		cls.test_user2 = User.objects.create_user(
			username='test_user2',
			email='testuser2-email@test.ru',
			password='testuser2_password',
		)

		cls.test_user3 = User.objects.create_user(
			username='test_user3',
			email='testuser3-email@test.ru',
			password='testuser3_password',
		)

		# Anonymous and authenticated users.
		cls.guest_user = Client()
		cls.authorized_user1 = Client().login(username='test_user1', password='testuser1_password')
		cls.authorized_user2 = Client().login(username='test_user2', password='testuser2_password')
		cls.authorized_user3 = Client().login(username='test_user3', password='testuser3_password')

		# Add tasks to db.
		cls.task1_user1 = Task.objects.create(
			title='Task1 by user1',
			description='Task1 by user1 description',
			due_date=datetime.date(2025, 12, 5),
			owner=cls.test_user1,
		)
		cls.task2_user1 = Task.objects.create(
			title='Task2 by user1',
			description='Task2 by user1 description',
			owner=cls.test_user1,
		)
		cls.task3_user1 = Task.objects.create(
			title='Task3 by user1',
			description='Task3 by user1 description',
			owner=cls.test_user1,
		)

		cls.task1_user2 = Task.objects.create(
			title='Task1 by user2',
			description='Task1 by user2 description',
			owner=cls.test_user2,
		)
		cls.task2_user2 = Task.objects.create(
			title='Task2 by user2',
			description='Task2 by user2 description',
			owner=cls.test_user2,
		)
		cls.task1_user3 = Task.objects.create(
			title='Task1 by user3',
			description='Task1 by user3 description',
			owner=cls.test_user3,
		)
		cls.personal_list_user1 = PersonalList.objects.create(
			title='Personal list by user1',
			description='Personal list by user1 description',
			owner=cls.test_user1,
		)

		cls.personal_list_user1.tasks.set([cls.task1_user1, cls.task2_user1])

	@classmethod
	def tearDownClass(cls):
		super().tearDownClass()

	def error_msg(self):
		error_msg = f'\n-------- Ошибка в тесте: {self.id()} --------'
		return error_msg
