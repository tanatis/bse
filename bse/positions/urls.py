from django.urls import path

from bse.positions.views import create_position

urlpatterns = [
    path('position/add/<int:pk>/', create_position, name='position_create'),
]
