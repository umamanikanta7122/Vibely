from django import forms
from .models import Post, Comment, Story

class PostForm(forms.ModelForm):


 class Meta:
    model = Post
    fields = [
        'caption',
        'media'
 ]


class CommentForm(forms.ModelForm):


  class Meta:
    model = Comment
    fields = ['text']


class StoryForm(forms.ModelForm):


  class Meta:
    model = Story
    fields = [
        'media',
        'caption'
    ]

