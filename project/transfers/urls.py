from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.TransfersCreate.as_view(), name='transfer-create'),
    path('list/', views.TransfersList.as_view(), name='transfer-list'),
]
