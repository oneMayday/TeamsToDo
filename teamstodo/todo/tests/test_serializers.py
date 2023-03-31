from datetime import datetime, date

from django.urls import reverse
from rest_framework import status

from ..models import Task, TeamList
from ..serializers import TaskSerializer, UpdateTaskSerializer, TeamListSerializer, CreateTeamListSerializer, \
	CreateTaskSerializer
from ..tests.test_settings import Settings
from ..views import TeamListAPIView


class TeamListSerializersTestCase(Settings):
	def test_teamlist_serializer(self) -> None:
		serializer = TeamListSerializer(self.team_list3)
		expected_data = {
			'pk': self.team_list3.pk,
			'title': 'Team list3',
			'description': 'Team list3 description',
			'tasks': [
				str(self.task1_user5),
			],
			'owner': self.test_user5.username,
			'members': [self.test_user5.pk],
		}

		self.assertEqual(serializer.data, expected_data, self.error())

	def test_create_teamlist_serializer(self) -> None:
		serializer = CreateTeamListSerializer(self.team_list3)
		expected_data = {
			'title': self.team_list3.title,
			'description': self.team_list3.description,
			'members': [self.test_user5.pk],
		}

		self.assertEqual(serializer.data, expected_data, self.error())

	def test_task_serializer(self) -> None:
		serializer = TaskSerializer(self.task1_user5)
		expected_data = {
			'id': self.task1_user5.pk,
			'teamlist_relation': self.team_list3.title,
			'who_takes': self.test_user5.username,
			'title': self.task1_user5.title,
			'status': self.task1_user5.status,
			'due_date': self.task1_user5.due_date,
			'owner': self.test_user5.pk,
		}

		self.assertEqual(serializer.data, expected_data, self.error())

	def test_createtask_serializer(self) -> None:
		serializer = CreateTaskSerializer(self.task1_user5)
		expected_data = {
			'id': self.task1_user5.pk,
			'title': self.task1_user5.title,
			'status': self.task1_user5.status,
			'due_date': self.task1_user5.due_date,
			'who_takes': self.test_user5.pk,
			'teamlist_relation': self.team_list3.pk,

		}

		self.assertEqual(serializer.data, expected_data, self.error())

	def test_updatetask_serializer(self) -> None:
		serializer = UpdateTaskSerializer(self.task1_user5)
		expected_data = {
			'status': self.task1_user5.status,
			'who_takes': self.test_user5.pk,
			'teamlist_relation': self.team_list3.pk,
		}

		self.assertEqual(serializer.data, expected_data, self.error())