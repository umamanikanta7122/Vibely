from django.urls import path
from .views import follow_user, home, register, profile, user_profile
from .views import home, register, profile, edit_profile
user_profile
follow_user
from .views import logout_user

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    path(
    'edit-profile/',
    edit_profile,
    name='edit_profile'
),

path(
    'user/<str:username>/',
    user_profile,
    name='user_profile'
),

path(
    'follow/<str:username>/',
    follow_user,
    name='follow_user'
),
path(
    'logout/',
    logout_user,
    name='logout'
),
]