from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from .models import Task, TeamList


class TaskSerializer(ModelSerializer):
	owner = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = Task
		fields = ('title', 'status', 'due_date', 'owner', 'teamlist_relation')


class TeamListSerializer(ModelSerializer):
	owner = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = TeamList
		fields = ('title', 'description', 'tasks', 'owner', 'members')
