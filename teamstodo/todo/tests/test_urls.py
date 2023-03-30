from django.urls import reverse

from rest_framework import status

from ..tests.test_settings import Settings


class UrlsTestCase(Settings):
	def test_teamlist_additional_url_all_tasks(self) -> None:
		url = reverse(f'teamlist-detail', args=(self.team_list2.pk, )) + 'all_tasks/'
		response = self.authorized_user1.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())

	def test_all_users_tasks(self) -> None:
		url = reverse(f'tasks-list') + 'my_tasks/'
		response = self.authorized_user2.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK, self.error())
