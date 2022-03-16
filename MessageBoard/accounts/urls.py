from django.urls import path
from .views import register_request, verify_registration
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('register/', register_request, name='register'),
    path('login/', LoginView.as_view(template_name ='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirmation/<int:user_id>/', verify_registration, name='confirmation'),
    ]