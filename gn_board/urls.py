from django.urls import path

from .views import *

urlpatterns = [
    path('', board, name='board'),
    path('detail/update/<int:pk>', boardEdit, name='edit'),
    path('delete/<int:pk>', boardDelete, name='delete'),
    path('create/', boardCreate, name='create'),
    path('detail/<int:pk>', dDetail, name='detail')
]