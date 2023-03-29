from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer, StringRelatedField

from .models import Task, TeamList


class TaskSerializer(ModelSerializer):
	teamlist_relation = StringRelatedField(many=False)
	who_takes = StringRelatedField(many=False)

	class Meta:
		model = Task
		exclude = ('create_date', 'update_date',)


class CreateTaskSerializer(ModelSerializer):
	"""Task serializer for create and update."""
	owner = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = Task
		exclude = ('create_date', 'update_date',)


class UpdateTaskSerializer(ModelSerializer):
	"""Task serializer for partial-update."""
	class Meta:
		model = Task
		fields = ('status', 'who_takes', 'teamlist_relation')


class TeamListSerializer(ModelSerializer):
	tasks = StringRelatedField(many=True)
	owner = StringRelatedField(many=False)

	class Meta:
		model = TeamList
		fields = ('pk', 'title', 'description', 'tasks', 'owner', 'members',)


class CreateTeamListSerializer(ModelSerializer):
	"""
	Teamlist serializer for creating teamlist.
	Without any tasks (tasks could be added later).
	"""
	owner = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = TeamList
		fields = ('title', 'description', 'owner', 'members')
