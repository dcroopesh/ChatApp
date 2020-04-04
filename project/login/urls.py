from django.urls import path , include
#from django.conf.urls import url
from .views import *
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

urlpatterns = [
    path('', RegistrationApiView.as_view(),name = 'user_register' ),
    path('login/',  LoginAPIview.as_view(),name = 'user_login' ),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('activate/<str:url>',Activate.as_view(),name = 'user_activate'),
    path('reset/password-link',ResetLinkView.as_view(),name = 'reset_link'),
    path('reset/password/<str:url>',ResetPasswordView.as_view(),name = 'reset_password'),
    path('logout/', logout_view,name = 'user_logout'),
    

]

