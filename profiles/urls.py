from django.urls import path
from .views import ProfileView

urlpatterns = [
    path('profiles/', ProfileView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
]
#pepchecked