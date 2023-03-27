from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TaskAPIView, TeamListAPIView

# Routers
router_tasks, router_team_list = DefaultRouter(), DefaultRouter()

router_tasks.register(r'tasks', TaskAPIView, basename='tasks')
router_team_list.register(r'teamlist', TeamListAPIView, basename='teamlist')

urlpatterns = [
	path('api-auth/', include('rest_framework.urls')),
	path('', include(router_tasks.urls)),
	path('', include(router_team_list.urls)),
]
