from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views as auth_views
from .views import *


urlpatterns = [
    path('index', auth_views.index, name='home'),
    path('registration/', registration, name='registration'),
    path('login/', auth_views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:status>', profile, name='profile'),
    path('profile/<str:status>', app_filter, name='app_filter'),
]