from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Task, TeamList
from .permissions import IsOwner, IsNotOwner
from .serializers import TaskSerializer, TeamListSerializer, CreateTaskSerializer, UpdateTaskSerializer, \
	CreateTeamListSerializer


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
		if self.action in ['create', 'partial-update']:
			serializer_class = CreateTaskSerializer
		elif self.action == 'update':
			serializer_class = UpdateTaskSerializer
		else:
			serializer_class = TaskSerializer
		return serializer_class

	def get_permissions(self):
		if self.action in ['destroy', 'partial_update']:
			permission_classes = [IsAuthenticated, IsOwner]
		elif self.action == 'update':
			permission_classes = [IsAuthenticated, IsNotOwner]
		else:
			permission_classes = [IsAuthenticated]
		return [permission() for permission in permission_classes]

	def create(self, request, *args, **kwargs):  #works
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

	# @action(methods=['PUT', 'PATCH'], detail=False)
	# def take_task(self, request, pk=None):
	# 	instance = self.get_object()
	# 	serializer = self.get_serializer(instance, data=request.data)
	# 	serializer.is_valid(raise_exception=True)
	# 	serializer.save()
	# 	return Response(serializer.data)


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
		tasks = Task.objects.select_related('teamlist_relation').filter(teamlist_relation_id=pk)
		serializer = TaskSerializer(tasks, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
