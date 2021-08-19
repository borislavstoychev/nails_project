from django.urls import path

from nails_project.nails import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home page'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('feedback/', views.FeedbackListView.as_view(), name='feedback list'),
    path('feedback-details/<int:pk>/', views.FeedbackDetailsView.as_view(), name='feedback details'),
    path('feedback-like/<int:pk>/', views.FeedbackLikeView.as_view(), name='feedback like'),
    path('feedback-create/', views.FeedbackCreateView.as_view(), name='feedback create'),
    path('feedback-edit/<int:pk>', views.FeedbackEditView.as_view(), name='feedback edit'),
    path('feedback-delete/<int:pk>', views.FeedbackDeleteView.as_view(), name='feedback delete'),
]
