from django.urls import path

from todo.views import TaskAPIView, PersonalListAPIView


urlpatterns = [
	path(r'tasks', TaskAPIView.as_view(), name='tasks'),
	path(r'personallist', PersonalListAPIView.as_view(), name='personallist'),
]
