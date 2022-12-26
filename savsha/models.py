from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Category(models.Model):
    user_id = models.IntegerField()
    category_names = models.CharField(max_length=1000)


class Friends(models.Model):
    user_id = models.IntegerField()
    friend_ids = models.CharField(max_length=1000)


class Contents(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=1000, default='previous ')
    last_name = models.CharField(max_length=1000, default='content')
    title = models.CharField(max_length=150)
    message = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    labels = models.CharField(max_length=1000)
    likes = models.ManyToManyField(User, related_name="contents")
