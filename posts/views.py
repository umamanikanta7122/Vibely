from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import PostForm
from .models import Post
from .models import Like

from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from django.db.models import Q
from .models import Story
from .forms import StoryForm
from .models import Story


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

    return redirect(request.META.get('HTTP_REFERER', '/'))

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

    return redirect('/')

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

    print("COMMENT VIEW HIT")

    post = Post.objects.get(id=post_id)

    if request.method == 'POST':

        form = CommentForm(request.POST)

        print("POST DATA:", request.POST)

        if form.is_valid():

            print("FORM VALID")

            comment = form.save(commit=False)

            comment.user = request.user
            comment.post = post

            comment.save()

            print("COMMENT SAVED")

        else:

            print(form.errors)

    return redirect('/')

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