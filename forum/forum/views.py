from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from .models import Topic, Post, Vote, UserMeta, Member, BaseUser, Admin, UserFactory

def topics(request):
    topicList = Topic.objects.all()
    context = {
            'topics': topicList
    }
    return render(request, 'forum/home.html', context)


def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    postList = Post.objects.filter(topic=topic, parent=None)
    context = {
        'topic': topic,
        'posts': postList,
    }
    return render(request, 'forum/topic.html', context)


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.parent:
        return redirect(reverse('post', args=(post.parent.id,)) + "#post-" + str(post.id))

    replies = Post.objects.filter(parent=post)
    context = {
        'post': post,
        'replies': replies,
    }
    return render(request, 'forum/post.html', context)


def user(request, user_id):
    userModel = get_object_or_404(User, id=user_id)

    user = UserFactory().create(userModel)

    context = {
        'userPage': user,
    }
    return render(request, 'forum/user.html', context)


def user_edit(request):
    if request.method != 'POST':
        meta, c = UserMeta.objects.get_or_create(user=request.user, key='page')
        return render(request, 'forum/user_edit.html', {'value': meta.value})

    user = UserFactory().create(request.user)
    user.setPersonalPage(request.POST['value'])

    return HttpResponseRedirect(reverse('user', args=(user.getId(),)))


@login_required
def vote(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post.toggleVote(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def new_thread(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    context = {
        'topic': topic,
    }
    return render(request, 'forum/new_post.html', context)


@login_required
def create_post(request):
    if request.method != 'POST':
        return HttpResponse('Only POST supported')

    if 'topic' in request.POST:
        topic = get_object_or_404(Topic, id=request.POST['topic'])
        post = Post(
                user = request.user,
                topic = topic,
                title = request.POST['title'],
                text  = request.POST['text'],
                )
        post.save()
        return HttpResponseRedirect(reverse('topic', args=(topic.id,)))

    if 'parent' in request.POST:
        parent = get_object_or_404(Post, id=request.POST['parent'])
        post = Post(
                user = request.user,
                parent = parent,
                text  = request.POST['text'],
                )
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required
def new_topic(request):
    if request.method != 'POST':
        return render(request, 'forum/new_topic.html', {})
    
    topic = Admin(request.user).createTopic(request.POST['name'])
    topic.save()

    return HttpResponseRedirect(reverse('topic', args=(topic.id,)))


def signup(request):
    if request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form':form})
