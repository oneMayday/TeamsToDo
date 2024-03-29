from django.test import TestCase
from django.test.client import Client

from todo.models import Task, TeamList
from users.models import User


class Settings(TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()

		# Add users to db and register them.
		# User5, task1_user5 and teamlist 3 - only for test_serializers.
		cls.test_user1 = User.objects.create_user(
			username='test_user1',
			email='testuser1-email@test.ru',
			password='testuser1_password',
		)
		cls.authorized_user1 = Client()
		cls.authorized_user1.login(username='test_user1', password='testuser1_password')

		cls.test_user2 = User.objects.create_user(
			username='test_user2',
			email='testuser2-email@test.ru',
			password='testuser2_password',
		)
		cls.authorized_user2 = Client()
		cls.authorized_user2.login(username='test_user2', password='testuser2_password')

		cls.test_user3 = User.objects.create_user(
			username='test_user3',
			email='testuser3-email@test.ru',
			password='testuser3_password',
		)
		cls.authorized_user3 = Client()
		cls.authorized_user3.login(username='test_user3', password='testuser3_password')

		cls.test_user4 = User.objects.create_user(
			username='test_user4',
			email='testuser4-email@test.ru',
			password='testuser4_password',
		)
		cls.authorized_user4 = Client()
		cls.authorized_user4.login(username='test_user4', password='testuser4_password')

		cls.test_user5 = User.objects.create_user(
			username='test_user5',
			email='testuser5-email@test.ru',
			password='testuser5_password',
		)
		cls.authorized_user5 = Client()
		cls.authorized_user5.login(username='test_user5', password='testuser5_password')

		# Anonymous user.
		cls.guest_user = Client()

		# Add test teamlists to db
		cls.team_list1 = TeamList.objects.create(
			title='Team list1',
			description='Team list1 description',
			owner=cls.test_user1
		)
		cls.team_list1.members.set([cls.test_user1, cls.test_user2])

		cls.team_list2 = TeamList.objects.create(
			title='Team list2',
			description='Team list2 description',
			owner=cls.test_user3,
		)
		cls.team_list2.members.set([cls.test_user1, cls.test_user3, cls.test_user4])

		cls.team_list3 = TeamList.objects.create(
			title='Team list3',
			description='Team list3 description',
			owner=cls.test_user5, )

		cls.team_list3.members.set([cls.test_user5,])

		# Add tasks to db.
		cls.task1_user1 = Task.objects.create(
			title='Task1 by user1',
			status=True,
			owner=cls.test_user1,
			who_takes=cls.test_user1,
			teamlist_relation=cls.team_list1,
		)
		cls.task2_user1 = Task.objects.create(
			title='Task2 by user1',
			owner=cls.test_user1,
			teamlist_relation=cls.team_list1,
		)
		cls.task3_user1 = Task.objects.create(
			title='Task3 by user1',
			owner=cls.test_user1,
			who_takes=cls.test_user3,
			teamlist_relation=cls.team_list2,
		)
		cls.task1_user2 = Task.objects.create(
			title='Task1 by user2',
			owner=cls.test_user2,
			teamlist_relation=cls.team_list1,
		)
		cls.task2_user2 = Task.objects.create(
			title='Task2 by user2',
			owner=cls.test_user2,
			teamlist_relation=cls.team_list1,
		)
		cls.task1_user3 = Task.objects.create(
			title='Task1 by user3',
			owner=cls.test_user3,
			who_takes=cls.test_user1,
			teamlist_relation=cls.team_list2,
		)
		cls.task1_user4 = Task.objects.create(
			title='Task1 by user4',
			status=True,
			owner=cls.test_user4,
			who_takes=cls.test_user1,
			teamlist_relation=cls.team_list2,
		)

		cls.task1_user5 = Task.objects.create(
			title='Task1 by user5',
			status=True,
			owner=cls.test_user5,
			who_takes=cls.test_user5,
			teamlist_relation=cls.team_list3,
		)

	@classmethod
	def tearDownClass(cls) -> None:
		super().tearDownClass()

	def error(self) -> str:
		error_lenght = len(str(self.id()))
		error_msg = f'\n{24 * "-" + error_lenght * "-"}\n' \
					f'--- Ошибка в тесте: {self.id()} ---\n' \
					f'{24 * "-" + error_lenght * "-"}'
		return error_msg
