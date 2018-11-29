from django.contrib import admin

from .models import Topic, Post, Vote, UserMeta

admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(UserMeta)
