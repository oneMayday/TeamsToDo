from django.urls import reverse

from rest_framework.test import APITestCase

from todo.serializers import TaskSerializer, PersonalListSerializer
from todo.tests.test_settings import Settings


class TaskApiTestCase(Settings, APITestCase):
	def test_get(self):
		"""Test get request for auth and guest users"""
		url = reverse('tasks')
		serializer_data = TaskSerializer([self.task1_user1, self.task2_user1, self.task3_user1], many=True).data

		response = self.authorized_user1.get(url)
		self.assertEqual(response.data, serializer_data, self.error_msg())

		response = self.guest_user.get(url)
		self.assertFalse(response.data, self.error_msg())


class PersonalListApiTestCase(Settings, APITestCase):
	def test_get(self):
		"""Test get request for auth and guest users"""
		url = reverse('personallist')
		serializer_data = PersonalListSerializer([self.personal_list_user1], many=True).data

		response = self.authorized_user1.get(url)
		self.assertEqual(response.data, serializer_data, self.error_msg())

		response = self.guest_user.get(url)
		self.assertFalse(response.data, self.error_msg())
