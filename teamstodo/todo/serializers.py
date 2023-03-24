from rest_framework.fields import HiddenField, CurrentUserDefault, CharField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Task, TeamList


class TaskSerializer(ModelSerializer):
	class Meta:
		model = Task
		fields = ('pk', 'title', 'status', 'due_date', 'teamlist_relation', 'who_takes')


class CreateTaskSerializer(ModelSerializer):
	owner = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = Task
		fields = ('pk', 'title', 'status', 'due_date', 'teamlist_relation', 'owner')


class UpdateTaskSerializer(ModelSerializer):
	who_takes = CurrentUserDefault()

	class Meta:
		model = Task
		fields = ('status', 'who_takes')


class TeamListSerializer(ModelSerializer):
	owner = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = TeamList
		fields = ('pk', 'title', 'description', 'tasks', 'owner', 'members')


class CreateTeamListSerializer(ModelSerializer):
	"""Create teamlist without any tasks (tasks can be added later)"""
	owner = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = TeamList
		fields = ('title', 'description', 'owner', 'members')
