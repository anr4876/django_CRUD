from django.urls import path

from .views import *

urlpatterns = [
    path('', board, name='board'),
    path('detail/update/<int:pk>', boardEdit, name='edit'),
    path('delete/<int:pk>', boardDelete, name='delete'),
    path('create/', boardCreate, name='create'),
    path('detail/<int:pk>', dDetail, name='detail'),
    path('download/<int:pk>', board_download_view,  name="board_download"),
    path('detail/createScv/<int:pk>', ex_download_view,  name="ex_download"),
]