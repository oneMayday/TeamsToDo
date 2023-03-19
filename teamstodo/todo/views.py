from django.shortcuts import render

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, PersonalList
from .serializers import TaskSerializer, PersonalListSerializer


class TaskAPIView(APIView):
	serializer_class = TaskSerializer

	def get(self, request):
		user = self.request.user
		all_users_tasks = Task.objects.filter(owner=user.pk)
		serializer = TaskSerializer(all_users_tasks, many=True)
		return Response(serializer.data)

	# def post(self):
	# 	return Response
	# # def post(self, request):


class PersonalListAPIView(APIView):
	serializer_class = PersonalListSerializer

	def get(self, request):
		user = self.request.user
		all_personal_lists = PersonalList.objects.filter(owner=user.pk)
		serializer = PersonalListSerializer(all_personal_lists, many=True)
		return Response(serializer.data)
