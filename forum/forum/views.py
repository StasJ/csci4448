from django.shortcuts import render

from .models import Topic, Post

def topics(request):
    topicList = Topic.objects.all()
    context = {
            'topics': topicList
    }
    return render(request, 'forum/topics.html', context)


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    postList = Post.objects.filter(topic=topic, parent=None)
    context = {
        'topic': topic,
        'posts': postList,
    }
    return render(request, 'forum/topic.html', context)

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    replies = Post.objects.filter(parent=post)
    context = {
        'post': post,
        'replies': replies,
    }
    return render(request, 'forum/post.html', context)
