from rest_framework.permissions import BasePermission, SAFE_METHODS

from todo.models import TeamList


class IsOwner(BasePermission):
	def has_object_permission(self, request, view, obj):
		return request.user == obj.owner


class TaskIsUserInMembership(BasePermission):
	def has_object_permission(self, request, view, obj):
		user = request.user

		membership = TeamList.objects\
			.prefetch_related('tasks')\
			.prefetch_related('members')\
			.filter(tasks__id=obj.pk)\
			.filter(members__id=user.pk)
		return True if membership else False


class TeamListMembeship(BasePermission):
	def has_object_permission(self, request, view, obj):
		user = request.user
		membership = TeamList.objects.prefetch_related('members').filter(members__id=user.pk)
		return True if membership else False
