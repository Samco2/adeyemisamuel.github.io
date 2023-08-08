from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .decorators import *
from django.contrib import messages

# sending email from contact
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


from .models import *
from .forms import PostForm
from .filters import PostFilter


def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:10]
    context = {'posts': posts}
    return render(request, 'base/index.html', context)


def projects(request):
    posts = Post.objects.filter(active=True)
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs
    page = request.GET.get('page')
    paginator = Paginator(posts, 2)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'myFilter': myFilter}

    return render(request, 'base/projects.html', context)


def project(request, slug):
    post = Post.objects.get(slug=slug)

    # Getting feedback on each detail project
    if request.method == 'POST':
        PostComment.objects.create(
            author=request.user.profile,
            post=post,
            body=request.POST['comment']
        )
        messages.success(request, "You're comment was successfuly posted!")
        return redirect('project', slug=post.slug)

    context = {'post': post}
    return render(request, 'base/project.html', context)


def profile(request):
    return render(request, 'base/profile.html')

# CRUD VIEWS


@admin_only
@login_required(login_url="home")
def createPost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('projects')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)


@admin_only
@login_required(login_url="home")
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('projects')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)


@admin_only
@login_required(login_url="home")
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'item': post}
    return render(request, 'base/delete.html', context)


def sendEmail(request):

    if request.method == 'POST':

        template = render_to_string('base/email_template.html', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['adeyemisamuela@gmail.com']
        )

        email.fail_silently = False
        email.send()

    return render(request, 'base/email_sent.html')
