from django.urls import path

from nails_project.nails import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home page'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('feedback/', views.NailsListView.as_view(), name='list nails'),
    path('details/<int:pk>/', views.NailsDetailsView.as_view(), name='nails details'),
    path('like/<int:pk>/', views.NailsLikeView.as_view(), name='like nails'),
    path('create/', views.NailsCreateView.as_view(), name='create nails'),
    path('edit/<int:pk>', views.NailsEditView.as_view(), name='edit nails'),
    path('delete/<int:pk>', views.NailsDeleteView.as_view(), name='delete nails'),
]
