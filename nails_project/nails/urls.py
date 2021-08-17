from django.urls import path

from nails_project.nails.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home page'),
]