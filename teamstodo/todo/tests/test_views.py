from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from ..models import Task
from ..tests.test_settings import Settings
from ..views import TeamListAPIView, TaskAPIView


class TeamlistViewTestCase(Settings):
	"""
	Teamlist API view test cases.
	Includes 'get', 'post', 'put', 'patch' and 'delete' methods.
	"""
	def test_get_teamlist_list_positive(self) -> None:
		# Only positive case.
		# Non authorized user cant get teamlist because permissions (see test_permissions).
		url = reverse('teamlist-list')

		# Test_user1 is in 2 teamlists.
		response = self.authorized_user1.get(url)
		expected_teamlist = [self.team_list1.title, self.team_list2.title]
		response_teamlist = find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_teamlist, expected_teamlist, self.error())

		# Test_user3 is in 1 teamlist.
		response = self.authorized_user3.get(url)
		expected_teamlist = [self.team_list2.title]
		response_teamlist = find_values_in_response_data(response, 'title')

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

	def test_get_teamlist_detail_positive(self) -> None:
		# Test_user1 can get test teamlist1.
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,))
		response = self.authorized_user1.get(url)
		expected_teamlist = self.team_list1.title
		response_teamlist = find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_teamlist, expected_teamlist, self.error())

		# Test_user3 can get test teamlist2.
		url = reverse(f'teamlist-detail', args=(self.team_list2.pk,))
		response = self.authorized_user3.get(url)
		expected_teamlist = self.team_list2.title
		response_teamlist = find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_teamlist, expected_teamlist, self.error())

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
		# Non-owner cat put changes.
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
		# Owner can put changes.
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
		# Non-owner can't patch teamlist.
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
		# Owner can patch teamlist.
		request_data = {
			'title': 'test_teamlist3',
			'description': 'test_teamlist3 description',
			'members': (self.test_user1.pk, self.test_user4.pk),
		}
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,))
		response = self.authorized_user1.patch(url, json=request_data)

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())

	def test_delete_teamlist_negative(self) -> None:
		# Non-owner can't delete teamlist.
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,),)
		response = self.authorized_user2.delete(url)
		detail_error_string = 'You do not have permission to perform this action.'

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, self.error())
		self.assertEqual(response.data['detail'], detail_error_string, self.error())

	def test_delete_teamlist_positive(self) -> None:
		# Only owner can delete teamlist.
		url = reverse(f'teamlist-detail', args=(self.team_list1.pk,),)
		response = self.authorized_user1.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, self.error())

	def test_all_tasks_teamlist(self) -> None:
		url = reverse(f'teamlist-detail', args=(self.team_list2.pk, )) + 'all_tasks/'
		response = self.authorized_user1.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())


class TaskViewTestCase(Settings):
	"""
	Task API view test cases.
	Includes 'get', 'post', 'put', 'patch' and 'delete' methods.
	"""
	def test_get_tasks_list_positive(self) -> None:
		# Only positive case.
		# Non authorized user cant get tasks because permissions (see test_permissions).
		url = reverse('tasks-list')

		# Test_user1 get all tasks from teamlist1 and teamlist 2.
		response = self.authorized_user1.get(url)
		expected_tasks = [
			self.task1_user1.title,
			self.task1_user2.title,
			self.task1_user3.title,
			self.task1_user4.title,
			self.task2_user1.title,
			self.task2_user2.title,
			self.task3_user1.title,
		]
		response_tasks = find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(set(response_tasks), set(expected_tasks), self.error())

		# Test_user3 get tasks only from teamlist2.
		response = self.authorized_user3.get(url)
		expected_tasks = [
			self.task3_user1.title,
			self.task1_user3.title,
			self.task1_user4.title,
		]
		response_tasks = find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(set(response_tasks), set(expected_tasks), self.error())

	def test_get_task_detail_negative(self) -> None:
		# Test_user3 can't get task1_user1 from test_teamlist1.
		url = reverse(f'tasks-detail', args=(self.task1_user1.pk,))
		response = self.authorized_user3.get(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, self.error())

		# Test_user2 can't get task1_user3 from test_teamlist2.
		url = reverse(f'tasks-detail', args=(self.task1_user3.pk,))
		response = self.authorized_user2.get(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, self.error())

	def test_get_task_detail_positive(self) -> None:
		# Test_user1 can get detailed-view task (owner).
		url = reverse(f'tasks-detail', args=(self.task1_user1.pk,))
		response = self.authorized_user1.get(url)
		expected_task = self.task1_user1.title
		response_task = find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_task, expected_task, self.error())

		# Test_user3 can get detailed-view task from teamlist2 (not-owner).
		url = reverse(f'tasks-detail', args=(self.task1_user4.pk,))
		response = self.authorized_user3.get(url)
		expected_task = self.task1_user4.title
		response_task = find_values_in_response_data(response, 'title')

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(response_task, expected_task, self.error())

	def test_post_task_negative(self) -> None:
		# User can't post task if choose 'who_takes' != user or None.
		url = reverse(f'tasks-list')

		request_data = {
			'title': 'task2_user3',
			'who_takes': self.test_user1.pk,
			'teamlist_relation': self.team_list2.pk,
		}
		response = self.authorized_user3.post(url, request_data)
		error_string = 'Вы не можете назначить исполнителем другого пользователя.'

		self.assertEqual(response.status_code, status.HTTP_423_LOCKED, self.error())
		self.assertEqual(response.data, error_string, self.error())

		# User can't post task if not in teamlist membership.
		request_data = {
			'title': 'task2_user3',
			'teamlist_relation': self.team_list1.pk,
		}
		response = self.authorized_user3.post(url, request_data)
		error_string = 'У вас не прав для добавления задачи в этот список'

		self.assertEqual(response.status_code, status.HTTP_423_LOCKED, self.error())
		self.assertEqual(response.data, error_string, self.error())

	def test_post_task_positive(self) -> None:
		request_data = {
			'title': 'task2_user3',
			'teamlist_relation': self.team_list2.pk,
		}
		url = reverse(f'tasks-list')
		response = self.authorized_user3.post(url, request_data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED, self.error())

	def test_put_task_negative(self) -> None:
		# User can't put task if he's not owner.
		factory = APIRequestFactory()
		view = TaskAPIView.as_view({'put': 'update'})

		request_data = {
			'title': 'task1_user3_update',
			'teamlist_relation': self.team_list1.pk,
		}
		url = reverse(f'tasks-detail', args=(self.task1_user1.pk,))
		request = factory.put(url, request_data)
		force_authenticate(request, user=self.test_user2)
		response = view(request, pk=self.task1_user1.pk)
		detail_error_string = 'You do not have permission to perform this action.'

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, self.error())
		self.assertEqual(response.data['detail'], detail_error_string, self.error())

	def test_put_task_positive(self) -> None:
		# User can put task if he's owner.
		factory = APIRequestFactory()
		view = TaskAPIView.as_view({'put': 'update'})

		request_data = {
			'title': 'task1_user3_update',
			'teamlist_relation': self.team_list2.pk,
		}
		url = reverse(f'tasks-detail', args=(self.task1_user3.pk,))
		request = factory.put(url, request_data)
		force_authenticate(request, user=self.test_user3)
		response = view(request, pk=self.task1_user3.pk)

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())

	def test_patch_task_negative(self) -> None:
		# User can't change field 'who_takes' if specified someone other than himself or null
		# and if he's not owner.
		factory = APIRequestFactory()
		view = TaskAPIView.as_view({'patch': 'partial_update'})

		url = reverse(f'tasks-detail', args=(self.task1_user1.pk,))

		request_data = {
			'who_takes': self.test_user1.pk,
			'teamlist_relation': self.team_list1.pk,
		}
		request = factory.patch(url, request_data)
		force_authenticate(request, user=self.test_user2)
		response = view(request, pk=self.task1_user1.pk)

		self.assertEqual(response.status_code, status.HTTP_423_LOCKED, self.error())

	def test_patch_task_positive(self) -> None:
		# User can change fields 'who_takes' and 'status' if specified himself or null.
		factory = APIRequestFactory()
		view = TaskAPIView.as_view({'patch': 'partial_update'})
		url = reverse(f'tasks-detail', args=(self.task2_user1.pk,))

		request_data = {
			'status': True,
			'teamlist_relation': self.team_list1.pk,
		}
		request = factory.patch(url, request_data)
		force_authenticate(request, user=self.test_user2)
		response = view(request, pk=self.task2_user1.pk)

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())

	def test_delete_task_negative(self) -> None:
		url = reverse(f'tasks-detail', args=(self.task1_user1.pk,), )
		response = self.authorized_user2.delete(url)
		detail_error_string = 'You do not have permission to perform this action.'

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, self.error())
		self.assertEqual(response.data['detail'], detail_error_string, self.error())

	def test_delete_task_positive(self) -> None:
		url = reverse(f'tasks-detail', args=(self.task1_user1.pk,), )
		response = self.authorized_user1.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, self.error())

	def test_all_users_tasks(self) -> None:
		url = reverse(f'tasks-list') + 'my_tasks/'
		response = self.authorized_user2.get(url)
		users_tasks = set(Task.objects.filter(who_takes=self.test_user2.pk).values())

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
		self.assertEqual(set(response.data), users_tasks, self.error())


def find_values_in_response_data(response: Response, model_field: str) -> list:
	"""Unpack response data and check necessary fields."""

	response_data = response.data
	if isinstance(response_data, list):
		unpacked_values = [ordered_dict[model_field] for ordered_dict in response_data]
	else:
		unpacked_values = response_data[model_field]
	return unpacked_values
