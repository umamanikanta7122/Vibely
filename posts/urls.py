print("POSTS URLS LOADED")

from django.urls import path
from .views import add_comment, create_post, edit_post, post_detail, search
from .views import create_post, delete_post
from .views import (
    create_post,
    delete_post,
    like_post
)
add_comment
edit_post
search
from .views import create_story
from .views import story_detail
from .views import reels
from .views import user_story
from django.contrib.auth.views import LogoutView
from .views import chat_room
from . import views
from .views import messages_page


urlpatterns = [
    path(
        'create-post/',
        create_post,
        name='create_post'
    ),

    path(
    'delete-post/<int:post_id>/',
    delete_post,
    name='delete_post'
),
    path(
    'like-post/<int:post_id>/',
    like_post,
    name='like_post'
),

path(
    'comment/<int:post_id>/',
    add_comment,
    name='add_comment'
),

path(
    'edit-post/<int:post_id>/',
    edit_post,
    name='edit_post'
),

path(
    'search/',
    search,
    name='search'
),

path(
    'story/user/<str:username>/',
    user_story,
    name='user_story'
),

path(
    'post/<int:post_id>/',
    post_detail,
    name='post_detail'
),

path(
    'create-story/',
    create_story,
    name='create_story'
),

path(
    'story/<int:story_id>/',
    story_detail,
    name='story_detail'
),

path(
    'reels/',
    reels,
    name='reels'
),

path(
    'logout/',
    LogoutView.as_view(next_page='/'),
    name='logout'
),

path(
    'chat/<str:username>/',
    chat_room,
    name='chat_room'
),
path(
    "messages/",
    views.messages_page,
    name="messages"
),
path(
    "messages/",
    views.messages_page,
    name="messages"
),

]