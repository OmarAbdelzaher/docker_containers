from django.urls import path
from .views import *

urlpatterns = [
    path('register/', registerpage , name='register' ),
    path('login/', loginpage , name='login' ),
    path('landing/', landing ,name='landing'),
    path('logout/', logoutpage,name='logout'),
    path('containers/', ContainerList.as_view() ,name='receive'),
]