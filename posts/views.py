from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import PostForm, CommentForm, StoryForm
from .models import Post, Like, Comment, Story, Notification
from django.db.models import Q
from .models import ChatMessage

@login_required
def create_post(request):

 print("CREATE POST VIEW HIT")

 if request.method == 'POST':

    print("POST REQUEST RECEIVED")

    form = PostForm(
        request.POST,
        request.FILES
    )

    if form.is_valid():

        print("FORM VALID")

        post = form.save(commit=False)

        post.user = request.user

        post.save()

        print("POST SAVED")

        return redirect('/')

    else:

        print("FORM ERRORS:")
        print(form.errors)

 else:

    form = PostForm()

 return render(
    request,
    'posts/create_post.html',
    {'form': form}
 )



@login_required
def delete_post(request, post_id):

    post = Post.objects.get(
        id=post_id,
        user=request.user
    )

    post.delete()

    return redirect('/profile/')

@login_required
def like_post(request, post_id):

    post = Post.objects.get(
        id=post_id
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    )

    if like.exists():

        like.delete()

    else:

        Like.objects.create(
            user=request.user,
            post=post
        )

        # don't notify if liking own post
        if post.user != request.user:

            Notification.objects.create(
                user=post.user,
                sender=request.user,
                post=post,
                message="liked your post ❤️"
            )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            '/'
        )
    )

@login_required
def edit_post(request, post_id):

    post = Post.objects.get(
        id=post_id,
        user=request.user
    )

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            instance=post
        )

        if form.is_valid():

            form.save()

            return redirect('/profile/')

    else:

        form = PostForm(
            instance=post
        )

    return render(
        request,
        'posts/edit_post.html',
        {'form': form}
    )

def search(request):
    query = request.GET.get('q')

    posts = Post.objects.all()
    users = User.objects.all()
    if query:
        posts = Post.objects.filter(
            Q(caption__icontains=query) |
            Q(user__username__icontains=query)
        )

        users = User.objects.filter(
            username__icontains=query
        )

    return render(
        request,
        'posts/search.html',
        {
            'posts': posts,
            'users': users,
            'query': query
        }
    )



from django.shortcuts import get_object_or_404

def post_detail(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    return render(
        request,
        'posts/post_detail.html',
        {'post': post}
    )

@login_required
def add_comment(request, post_id):

    post = Post.objects.get(
        id=post_id
    )

    if request.method == 'POST':

        form = CommentForm(
            request.POST
        )

        if form.is_valid():

            comment = form.save(
                commit=False
            )

            comment.user = request.user
            comment.post = post

            comment.save()

            # notification only if commenting on another user's post
            if post.user != request.user:

                Notification.objects.create(
                    user=post.user,
                    sender=request.user,
                    post=post,
                    message=f'commented: "{comment.text}" 💬'
                )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            '/'
        )
    )
@login_required
def create_story(request):

    if request.method == 'POST':

        form = StoryForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            story = form.save(
                commit=False
            )

            story.user = request.user

            story.save()

            return redirect('/')

    else:

        form = StoryForm()

    return render(
        request,
        'posts/create_story.html',
        {'form': form}
    )

def story_detail(request, story_id):

    story = Story.objects.get(
        id=story_id
    )

    return render(
        request,
        'posts/story_detail.html',
        {'story': story}
    )


@login_required
def reels(request):

    videos = Post.objects.filter(
        media__iendswith='.mp4'
    ).order_by('-created_at')

    return render(
        request,
        'posts/reels.html',
        {'videos': videos}
    )

from .models import Story
from django.shortcuts import get_object_or_404

def user_story(request, username):

    print("USER STORY HIT", username)

    stories = Story.objects.filter(
        user__username=username
    )

    print("COUNT =", stories.count())

    return render(
        request,
        'posts/story_detail.html',
        {'stories': stories}
    )

@login_required
def chat_room(request, username):

    other_user = User.objects.get(
        username=username
    )

    room_name = (
        f"chat_"
        f"{min(request.user.id, other_user.id)}_"
        f"{max(request.user.id, other_user.id)}"
    )

    # GET OLD CHAT HISTORY
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by(
        "timestamp"
    )
    print("MESSAGES COUNT =", messages.count())
    return render(
        request,
        'posts/chat_room.html',
        {
            'room_name': room_name,
            'other_user': other_user,
            'messages': messages,
        }
    )

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def messages_page(request):

    users = User.objects.exclude(
        id=request.user.id
    )

    return render(
        request,
        "posts/messages.html",
        {
            "users": users
        }
    )