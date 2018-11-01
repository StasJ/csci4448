from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Post(models.Model):
    user   = models.ForeignKey(User,  on_delete=models.CASCADE)
    topic  = models.ForeignKey(Topic, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title  = models.CharField(max_length=256)
    text   = models.TextField()
    date   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if (self.parent):
            return "Reply to " + self.parent.title
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title + " : " + self.user.username
