from django.urls import path
from . import views

urlpatterns = [
	path('profile/<str:username>', views.profile, name="profile"),
	path('dashboard/', views.dashboard, name="dashboard")
]