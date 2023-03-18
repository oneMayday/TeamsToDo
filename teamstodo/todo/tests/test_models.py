from .test_settings import Settings


class TaskTestCase(Settings):
	def test_created_tasks_poles(self):
		self.assertEqual(self.task1_user1.title, 'Task1 by user1')
		self.assertEqual(self.task1_user1.description, 'Task1 by user1 description')
		self.assertEqual(self.task1_user1.owner, self.test_user1)

	def test_tasks_owners(self):
		self.assertEqual(self.task1_user1.owner, self.test_user1)
		self.assertEqual(self.task1_user2.owner, self.test_user2)
		self.assertEqual(self.task1_user3.owner, self.test_user3)

	# def test_meta_parametres(self):
	# 	self.assertEqual(self.task1_user3._Meta_.verbose_name, 'Задача')