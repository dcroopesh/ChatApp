from django.urls import path

from .views import *

urlpatterns = [
    path('',index, name='index'),
    path('p2p/',p2pIndex,name='p2p_index'),
    path('<str:room_name>/',roomm, name='room'),
    path('p2p/<str:receiver>/',p2pRoom, name='p2proom'),
    
]


