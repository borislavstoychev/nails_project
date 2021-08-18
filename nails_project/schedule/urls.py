
from django.urls import path

from nails_project.schedule import views

urlpatterns = [
    path('', views.ScheduleListView.as_view(), name='schedule view'),
    path('create-schedule/', views.ScheduleCreateView.as_view(), name='schedule create'),
    path('schedule-delete/<int:pk>', views.ScheduleDeleteView.as_view(), name='delete schedule'),

]