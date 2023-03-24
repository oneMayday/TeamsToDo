from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Task, TeamList
from .permissions import IsOwner, TaskIsUserInMembership, TeamListMembeship
from .serializers import TaskSerializer, TeamListSerializer, CreateTaskSerializer, UpdateTaskSerializer, \
	CreateTeamListSerializer


class TaskAPIView(ModelViewSet):
	permission_classes = [IsAuthenticated, ]

	def get_queryset(self):
		"""Get user's taken tasks"""
		user = self.request.user
		queryset = Task.objects.filter(who_takes=user.pk)
		return queryset

	def get_serializer_class(self):
		if self.action == 'create':
			serializer_class = CreateTaskSerializer
		elif self.action in ['partial-update', 'take_task']:
			serializer_class = UpdateTaskSerializer
		else:
			serializer_class = TaskSerializer
		return serializer_class

	# def get_permissions(self):
	# 	if self.action in ['list', 'retrieve', 'create']:
	# 		permission_classes = [IsAuthenticated, ]
	# 	elif self.action in ['destroy']:
	# 		permission_classes = [IsAuthenticated, IsOwner]
	# 	elif self.action in ['update', 'partial_update']:
	# 		permission_classes = [TaskIsUserInMembership]
	# 	else:
	# 		permission_classes = [IsAuthenticated]
	# 	return [permission() for permission in permission_classes]

	def create(self, request, *args, **kwargs):
		"""Create task if user in team list members."""
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
			raise Exception('У вас не прав для добавления задачи в этот список')

	@action(methods=['PUT', 'PATCH'], detail=True)
	def take_task(self, request):
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)


class TeamListAPIView(ModelViewSet):
	def get_queryset(self):
		"""Get teamlists, where user is in membership"""
		user = self.request.user
		queryset = TeamList.objects.prefetch_related('members').filter(members__pk=user.pk)
		return queryset

	def get_permissions(self):
		# Only teamlist owner could change teamlist properties.
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
		tasks = TeamList.objects.get(pk=pk).tasks
		serializer = TaskSerializer(tasks, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
