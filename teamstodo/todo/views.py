from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Task, TeamList
from .serializers import TaskSerializer, TeamListSerializer


class TaskAPIView(ModelViewSet):
	serializer_class = TaskSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		queryset = Task.objects.filter(owner=user.pk)
		return queryset

	def create(self, request, *args, **kwargs):
		"""Create task if user in team list members"""
		user = request.user
		target_teamlist = TeamList.objects.get(pk=request.data['teamlist_relation']).members.values('id')
		members = [member['id'] for member in target_teamlist]

		if user.pk in members:
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			self.perform_create(serializer)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
		else:
			raise Exception('Нельзя добавить задачу в список')


class TeamListAPIView(ModelViewSet):
	queryset = TeamList.objects.all()
	serializer_class = TeamListSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		queryset = TeamList.objects.select_related('owner')
		return queryset

