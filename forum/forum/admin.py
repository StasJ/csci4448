from django.contrib import admin

from .models import Topic, Post, Vote

admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Vote)
