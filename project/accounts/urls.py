from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.AccountsList.as_view(), name='accounts-list'),
]
