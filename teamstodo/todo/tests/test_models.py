from datetime import date

from .test_settings import Settings


class ModelTestCase(Settings):
	# Task model test cases.
	def test_tasks_fields(self) -> None:
		self.assertEqual(self.task1_user1.title, 'Task1 by user1', self.error())
		self.assertTrue(self.task1_user1.status, self.error())
		self.assertFalse(self.task1_user2.status, self.error())
		self.assertEqual(self.task1_user1.create_date, date.today(), self.error())
		self.assertEqual(self.task1_user1.update_date, date.today(), self.error())
		self.assertEqual(self.task1_user1.due_date, None, self.error())
		self.assertEqual(self.task1_user1.owner, self.test_user1, self.error())
		self.assertEqual(self.task1_user1.teamlist_relation, self.team_list1, self.error())

	def test_tasks_meta_poles(self) -> None:
		self.assertEqual(self.task1_user3._meta.verbose_name, 'Задача', self.error())
		self.assertEqual(self.task1_user3._meta.verbose_name_plural, 'Задачи', self.error())

	# TeamList model test cases
	def test_teamlist_field(self) -> None:
		self.assertEqual(self.team_list1.title, 'Team list1', self.error())
		self.assertEqual(self.team_list1.description, 'Team list1 description', self.error())
		self.assertEqual(self.team_list1.date_create, date.today(), self.error())
		self.assertEqual(self.team_list1.owner, self.test_user1, self.error())
		self.assertEqual(
			[member for member in self.team_list1.members.all()],
			[self.test_user1, self.test_user2],
			self.error()
		)

	def test_teamlist_meta_poles(self) -> None:
		self.assertEqual(self.team_list1._meta.verbose_name, 'Командный список', self.error())
		self.assertEqual(self.team_list2._meta.verbose_name_plural, 'Командные списки', self.error())
