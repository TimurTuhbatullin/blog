from django.urls import path, include
from . import views
app_name = 'user'

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("register/", views.register, name='register'),
    path("user/<int:user_id>", views.profile, name='profile'),
    path("logout", views.log_out, name="logout")
]
