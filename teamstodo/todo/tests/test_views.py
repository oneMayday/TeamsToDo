from collections import OrderedDict
from typing import Union

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from todo.tests.test_settings import Settings


class TeamlistViewTestCase(Settings):
	"""
	Teamlist API view test cases.
	Includes 'get', 'post', 'put', 'patch' and 'delete' methods.
	"""
	@staticmethod
	def find_values_in_response_data(response: Response, model_field: str) -> list:
		"""Unpack response data and check necessary fields."""
		response_data = response.data
		print(type(response_data))
		if isinstance(response_data, list):
			unpacked_values = [ordered_dict[model_field] for ordered_dict in response_data]
		else:
			unpacked_values = response_data[model_field]
		return unpacked_values

	def test_get_teamlist_list_positive(self) -> None:
		# Only positive cases.
		# Non authorized user cant get teamlist beacuse permissions (see test_permissions).
		url = reverse('teamlist-list')

		# Test_user1 is in 2 teamlists.
		response = self.authorized_user1.get(url)
		expected_teamlist = [self.team_list1.title, self.team_list2.title]
		response_teamlist = self.find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_teamlist, expected_teamlist, self.error())

		# Test_user3 is in 1 teamlist.
		response = self.authorized_user3.get(url)
		expected_teamlist = [self.team_list2.title]
		response_teamlist = self.find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_teamlist, expected_teamlist, self.error())

	def test_get_teamlist_detail_positive(self) -> None:
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk, ))

		# Test_user1 can get test teamlists.
		response = self.authorized_user1.get(url)
		expected_teamlist = self.team_list1.title
		response_teamlist = self.find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_teamlist, expected_teamlist, self.error())

		# Test_user3 can get test teamlists.
		response = self.authorized_user3.get(url)
		expected_teamlist = self.team_list2.title
		response_teamlist = self.find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_teamlist, expected_teamlist, self.error())

	def test_get_teamlist_detail_negative(self) -> None:
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk, ))
		# Test_user3 can't get test_teamlist1.
		response = self.authorized_user3.get(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, self.error())

		url = reverse(f'teamlist-detail', args=(self.team_list2.pk,))
		# Test_user2 cant get test_teamlist2.
		response = self.authorized_user2.get(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, self.error())

