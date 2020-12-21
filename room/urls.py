from django.urls import path
from .views import *

urlpatterns = [
    path('room/add', room_add),
    path('reserve/add', reserve_add),
    path('room/delete/<int:room_id>', room_delete),
    path('reserve/delete/<int:booking_id>', reserve_delete),
    path('rooms', get_all_room),
    path('reserve', get_all_reserve),
]