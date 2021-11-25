from django.contrib import admin

# Register your models here.
from nails_project.schedule.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time')
    list_filter = ('date', )
    ordering = ('date',)
