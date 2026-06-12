from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)

    location = models.CharField(
        max_length=100,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.user.username
    
    profile_picture = models.ImageField(
    upload_to='profile_pictures/',
    default='default.jpg'
)
    
    cover_photo = models.ImageField(
    upload_to='cover_photos/',
    blank=True,
    null=True
)
    
    from django.contrib.auth.models import User

class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    class Meta:
        unique_together = (
            'follower',
            'following'
        )