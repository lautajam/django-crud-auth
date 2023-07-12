from django.contrib import admin
from .models import Tasks

class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", )

# Shows the Tasks in admin
admin.site.register(Tasks, TasksAdmin)