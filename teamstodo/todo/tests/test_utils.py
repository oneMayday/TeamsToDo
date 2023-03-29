from todo.tests.test_settings import Settings

from todo.utils import validate_user_membership, validate_is_user_take_task


class UtilsTestCase(Settings):
	def test_validate_user_membership_negative(self):
		user = self.test_user3
		data = {'teamlist_relation': self.team_list1.pk}
		self.assertFalse(validate_user_membership(user, data), self.error())

	def test_validate_user_membership_positive(self):
		user = self.test_user1
		data = {'teamlist_relation': self.team_list1.pk}
		self.assertTrue(validate_user_membership(user, data), self.error())

	def test_validate_is_user_take_task_negative(self):
		user = self.test_user1
		data = {'who_takes': self.test_user2}
		self.assertFalse(validate_is_user_take_task(user, data), self.error())

	def test_validate_is_user_take_task_positive(self):
		user = self.test_user1
		data = {'who_takes': self.test_user1}
		self.assertFalse(validate_is_user_take_task(user, data), self.error())