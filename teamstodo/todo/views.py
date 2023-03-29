from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Task, TeamList
from .permissions import IsOwner
from .serializers import (
	CreateTaskSerializer,
	CreateTeamListSerializer,
	TaskSerializer,
	TeamListSerializer,
	UpdateTaskSerializer
)
from .utils import update_task_api_view, create_task_api_view


class TaskAPIView(ModelViewSet):
	queryset = Task.objects.all()
	# def get_queryset(self):  # works
	# 	"""Get user's taken tasks"""
	# 	user = self.request.user
	#
	# 	teamlist_queryset = TeamList.objects.prefetch_related('members').filter(members__pk=user.pk)
	# 	queryset = []
	# 	for tl in teamlist_queryset:
	# 		result = Task.objects.filter(teamlist_relation_id=tl.pk)
	# 		queryset.extend(result)
	# 	return queryset

	def get_serializer_class(self):
		if self.action in ['create', 'update']:
			serializer_class = CreateTaskSerializer
		elif self.action == 'partial_update':
			serializer_class = UpdateTaskSerializer
		else:
			serializer_class = TaskSerializer
		return serializer_class

	def get_permissions(self):
		if self.action in ['destroy', 'update']:
			permission_classes = [IsAuthenticated, IsOwner]
		else:
			permission_classes = [IsAuthenticated]
		return [permission() for permission in permission_classes]

	def create(self, request, *args, **kwargs):
		"""Create task if user in team list members."""
		data, accept_status = create_task_api_view(self, request, *args, **kwargs)
		if accept_status == 'accepted':
			return Response(data=data, status=status.HTTP_201_CREATED)
		else:
			return Response(data=data, status=status.HTTP_423_LOCKED)

	def update(self, request, *args, **kwargs):
		data, accept_status = update_task_api_view(self, request, *args, **kwargs)
		if accept_status == 'accepted':
			return Response(data=data, status=status.HTTP_200_OK)
		else:
			return Response(data=data, status=status.HTTP_423_LOCKED)

	@action(methods=['GET'], detail=False)
	def my_tasks(self, request):
		"""Get all tasks, that user takes."""
		tasks = Task.objects.filter(who_takes=request.user.pk)
		serializer = TaskSerializer(tasks, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class TeamListAPIView(ModelViewSet):
	def get_queryset(self):
		"""Get teamlists, where user is in membership."""
		user = self.request.user
		queryset = TeamList.objects.prefetch_related('members').filter(members__pk=user.pk)
		return queryset

	def get_permissions(self):
		if self.action in ['update', 'partial_update', 'destroy']:
			permission_classes = [IsAuthenticated, IsOwner]
		else:
			permission_classes = [IsAuthenticated]
		return [permission() for permission in permission_classes]

	def get_serializer_class(self):
		if self.action == 'create':
			serializer_class = CreateTeamListSerializer
		else:
			serializer_class = TeamListSerializer
		return serializer_class

	@action(detail=True, methods=['GET'])
	def all_tasks(self, request, pk):
		"""Get all teamlist's tasks."""
		tasks = Task.objects.select_related('teamlist_relation').filter(teamlist_relation_id=pk)
		serializer = TaskSerializer(tasks, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
