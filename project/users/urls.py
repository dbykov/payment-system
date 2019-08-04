from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('register/', views.UsersRegister.as_view(), name='users-register'),
    path('obtain-token/', obtain_auth_token, name='users-obtain-token'),
]
