from django.urls import path

from bse.positions.views import create_position, add_to_position, sell_position

urlpatterns = [
    path('position/create/<str:symbol>/', create_position, name='position_create'),
    path('position/add/<int:pk>/', add_to_position, name='position_add'),
    path('position/sell/<int:pk>/', sell_position, name='position_sell'),
]
