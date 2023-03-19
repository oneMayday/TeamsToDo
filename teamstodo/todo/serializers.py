from rest_framework.serializers import ModelSerializer

from .models import Task, PersonalList


class TaskSerializer(ModelSerializer):
	class Meta:
		model = Task
		fields = ('title', 'description', 'status', 'due_date')


class PersonalListSerializer(ModelSerializer):
	class Meta:
		model = PersonalList
		fields = ('title', 'description', 'tasks')
