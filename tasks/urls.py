from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.TaskView.as_view()),
    path('tasks/<int:pk>/', views.TaskView.as_view()),
]
