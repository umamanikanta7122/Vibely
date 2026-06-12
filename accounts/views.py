from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from httpx import request

import posts

from .forms import RegisterForm, ProfileForm
from .models import Profile, Follow
from posts.models import Post
from posts.models import Story
from posts.models import Notification


def home(request):

    for post in Post.objects.all():
        post.views += 1
        post.save()

    posts = Post.objects.all().order_by('-created_at')

    all_stories = Story.objects.all()

    seen_users = []
    stories = []

    for story in all_stories:

        if story.user not in seen_users:
            stories.append(story)
            seen_users.append(story.user)

    notification_count = 0
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    return render(
        request,
        'home.html',
        {
            'posts': posts,
            'stories': stories,
            'notification_count': notification_count
        }
    )


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    posts = Post.objects.filter(
        user=request.user
    ).order_by('-created_at')

    posts_count = posts.count()

    followers_count = Follow.objects.filter(
        following=request.user
    ).count()

    following_count = Follow.objects.filter(
        follower=request.user
    ).count()

    notification_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        'accounts/profile.html',
        {
            'profile': profile,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'posts_count': posts_count,
            'notification_count': notification_count
        }
    )


@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('/profile/')

    else:
        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'accounts/edit_profile.html',
        {'form': form}
    )


def user_profile(request, username):

    profile_user = User.objects.get(
        username=username
    )

    posts = Post.objects.filter(
        user=profile_user
    ).order_by('-created_at')

    is_following = False

    if request.user.is_authenticated:

        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    notification_count = 0
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    return render(
        request,
        'accounts/user_profile.html',
        {
            'profile_user': profile_user,
            'posts': posts,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'notification_count': notification_count
        }
    )


@login_required
def follow_user(request, username):

    user_to_follow = User.objects.get(
        username=username
    )

    if user_to_follow != request.user:

        follow = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow
        )

        if follow.exists():

            follow.delete()

        else:

            Follow.objects.create(
                follower=request.user,
                following=user_to_follow
            )

            print("CREATING NOTIFICATION")

    Notification.objects.create(
    user=user_to_follow,
    sender=request.user,
    message="started following you"
)

    return redirect(
        f'/user/{username}/'
    )


from django.contrib.auth import logout


def logout_user(request):
    logout(request)
    return redirect('/login/')


@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    notification_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        'notifications.html',
        {
            'notifications': notifications,
            'notification_count': notification_count
        }
    )