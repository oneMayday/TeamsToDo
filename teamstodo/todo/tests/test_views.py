from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from todo.tests.test_settings import Settings
from todo.views import TeamListAPIView
from users.models import User


class TeamlistViewTestCase(Settings):
	"""
	Teamlist API view test cases.
	Includes 'get', 'post', 'put', 'patch' and 'delete' methods.
	"""
	@staticmethod
	def find_values_in_response_data(response: Response, model_field: str) -> list:
		"""Unpack response data and check necessary fields."""
		response_data = response.data
		if isinstance(response_data, list):
			unpacked_values = [ordered_dict[model_field] for ordered_dict in response_data]
		else:
			unpacked_values = response_data[model_field]
		return unpacked_values

	def test_get_teamlist_list_positive(self) -> None:
		# Only positive cases.
		# Non authorized user cant get teamlist because permissions (see test_permissions).
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
		# Test_user1 can get test teamlist1.
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,))
		response = self.authorized_user1.get(url)
		expected_teamlist = self.team_list1.title
		response_teamlist = self.find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_teamlist, expected_teamlist, self.error())

		# Test_user3 can get test teamlist2.
		url = reverse(f'teamlist-detail', args=(self.team_list2.pk,))
		response = self.authorized_user3.get(url)
		expected_teamlist = self.team_list2.title
		response_teamlist = self.find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_teamlist, expected_teamlist, self.error())

	def test_get_teamlist_detail_negative(self) -> None:
		# Test_user3 can't get test_teamlist1.
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,))
		response = self.authorized_user3.get(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, self.error())

		# Test_user2 cant get test_teamlist2.
		url = reverse(f'teamlist-detail', args=(self.team_list2.pk,))
		response = self.authorized_user2.get(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, self.error())

	def test_post_teamlist_positive(self) -> None:
		# Only positive cases.
		# Non authorized user cant post teamlist beacuse permissions (see test_permissions).
		request_data = {
			'title': 'test_teamlist3',
			'description': 'test_teamlist3 description',
			'members': (self.test_user1.pk, self.test_user4.pk),
		}
		url = reverse(f'teamlist-list')
		response = self.authorized_user1.post(url, request_data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED, self.error())

	def test_put_teamlist_negative(self) -> None:
		request_data = {
			'title': 'test_teamlist3',
			'description': 'test_teamlist3 description',
			'members': (self.test_user1.pk, self.test_user4.pk),
		}
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,))
		response = self.authorized_user2.put(url, json=request_data)
		detail_error_string = 'You do not have permission to perform this action.'

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, self.error())
		self.assertEqual(response.data['detail'], detail_error_string, self.error())

	def test_put_teamlist_positive(self) -> None:
		factory = APIRequestFactory()
		view = TeamListAPIView.as_view({'put': 'update'})
		request_data = {
			'title': 'test_teamlist5',
			'members': (self.test_user1.pk, self.test_user2.pk, self.test_user3.pk)
		}
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,))
		request = factory.put(url, request_data)

		force_authenticate(request, user=self.test_user1)
		response = view(request, pk=self.team_list1.pk)

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())

	def test_patch_teamlist_negative(self) -> None:
		request_data = {
			'title': 'test_teamlist3',
			'description': 'test_teamlist3 description',
			'members': (self.test_user1.pk, self.test_user4.pk),
		}
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,))
		response = self.authorized_user2.patch(url, json=request_data)
		detail_error_string = 'You do not have permission to perform this action.'

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, self.error())
		self.assertEqual(response.data['detail'], detail_error_string, self.error())

	def test_patch_teamlist_positive(self) -> None:
		request_data = {
			'title': 'test_teamlist3',
			'description': 'test_teamlist3 description',
			'members': (self.test_user1.pk, self.test_user4.pk),
		}
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,))
		response = self.authorized_user1.patch(url, json=request_data)

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())

	# def test_delete_teamlist_negative(self) -> None:
	# 	# Not-owner can't delete teamlist
	# 	url = reverse(f'teamlist-detail', args=(self.team_list1.pk,),)
	# 	response = self.authorized_user2.delete(url)
	# 	detail_error_string = 'You do not have permission to perform this action.'
	#
	# 	self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, self.error())
	# 	self.assertEqual(response.data['detail'], detail_error_string, self.error())
	#
	# def test_delete_teamlist_positive(self) -> None:
	# 	# Only owner can delete teamlist.
	# 	url = reverse(f'teamlist-detail', args=(self.team_list1.pk,),)
	# 	response = self.authorized_user1.delete(url)
	#
	# 	self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, self.error())