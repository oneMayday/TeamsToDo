from datetime import date

from .test_settings import Settings


class TaskTestCase(Settings):
	"""Task model test cases"""
	def test_created_tasks_poles(self):
		self.assertEqual(self.task1_user1.title, 'Task1 by user1', self.error_msg())
		self.assertEqual(self.task1_user1.description, 'Task1 by user1 description', self.error_msg())
		self.assertFalse(self.task1_user1.status)
		self.assertEqual(self.task1_user1.due_date, date(2025, 12, 5), self.error_msg())
		self.assertEqual(self.task1_user1.owner, self.test_user1, self.error_msg())

	def test_meta_poles(self):
		self.assertEqual(self.task1_user3._meta.verbose_name, 'Задача', self.error_msg())
		self.assertEqual(self.task1_user3._meta.verbose_name_plural, 'Задачи', self.error_msg())


class PersonalListTestCase(Settings):
	"""PersonalList model test cases"""
	def test_created_personal_list_poles(self):
		self.assertEqual(self.personal_list_user1.title, 'Personal list by user1', self.error_msg())
		self.assertEqual(self.personal_list_user1.description, 'Personal list by user1 description', self.error_msg())
		self.assertEqual(
			[task for task in self.personal_list_user1.tasks.all()],
			[self.task1_user1, self.task2_user1],
			self.error_msg()
		)
		self.assertEqual(self.personal_list_user1.owner, self.test_user1, self.error_msg())

	def test_meta_poles(self):
		self.assertEqual(self.personal_list_user1._meta.verbose_name, 'Личный список', self.error_msg())
		self.assertEqual(self.personal_list_user1._meta.verbose_name_plural, 'Личные списки', self.error_msg())


class TeamListTestCase(Settings):
	"""TeamList model test cases"""
	def test_created_team_list(self):
		self.assertEqual(self.team_list.title, 'Team list', self.error_msg())
		self.assertEqual(self.team_list.description, 'Team list description', self.error_msg())
		self.assertEqual(
			[member for member in self.team_list.members.all()],
			[self.test_user1, self.test_user2, self.test_user3],
			self.error_msg()
		)
		self.assertEqual(
			[task for task in self.team_list.tasks.all()],
			[self.task1_user1, self.task1_user2, self.task1_user3],
			self.error_msg()
		)

	def test_meta_poles(self):
		self.assertEqual(self.team_list._meta.verbose_name, 'Командный список', self.error_msg())
		self.assertEqual(self.team_list._meta.verbose_name_plural, 'Командные списки', self.error_msg())