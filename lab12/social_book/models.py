from django.contrib.auth import get_user_model
from django.db import models
import uuid

from datetime import datetime

from django.urls import reverse

# Create your models here.
User = get_user_model()


class City(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book Author")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city', kwargs={'city_slug': self.slug})


class Interests(models.Model):
    name = models.CharField(max_length=200, help_text="Interests")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('interest', kwargs={'interest_slug': self.slug})


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    contacts = models.TextField(blank=True)
    number = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='profile.jpg')
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    interests = models.ManyToManyField(Interests, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    commenter_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.caption, self.commenter_name)
