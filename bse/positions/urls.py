from django.urls import path

from bse.positions.views import create_position

urlpatterns = [
    path('position/create/<str:symbol>/', create_position, name='position_create'),
]
