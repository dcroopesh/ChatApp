from django.urls import path

from .views import *

urlpatterns = [
    # path('',index, name='index'),
    # path('p2p/',p2pIndex,name='p2p_index'),
    # path('<str:room_name>/',roomm, name='room'),
    #path('p2p/<str:receiver>/',roomm, name='p2proom'),
    path('',p2pRoom.as_view(), name='room'),
    
]


