from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer, StringRelatedField

from .models import Task, TeamList


class TaskSerializer(ModelSerializer):
	teamlist_relation = StringRelatedField(many=False)
	who_takes = StringRelatedField(many=False)

	class Meta:
		model = Task
		fields = ('pk', 'title', 'status', 'due_date', 'teamlist_relation', 'who_takes', 'owner')


class CreateTaskSerializer(ModelSerializer):
	owner = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = Task
		fields = ('pk', 'title', 'status', 'due_date', 'teamlist_relation', 'owner')


class UpdateTaskSerializer(ModelSerializer):
	who_takes = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = Task
		fields = ('status', 'who_takes')


class TeamListSerializer(ModelSerializer):
	tasks = StringRelatedField(many=True)

	class Meta:
		model = TeamList
		fields = ('pk', 'title', 'description', 'tasks', 'owner', 'members')


class CreateTeamListSerializer(ModelSerializer):
	"""Create teamlist without any tasks (tasks could be added later)"""
	owner = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = TeamList
		fields = ('title', 'description', 'owner', 'members')
