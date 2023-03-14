from django.contrib import admin

from .models import Task, PersonalList, TeamList


admin.site.register(Task)
admin.site.register(PersonalList)
admin.site.register(TeamList)
