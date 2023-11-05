from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EventForm, CommentForm
from .models import Event, Category, User, Follow
from .utils import get_pagination


def index(request):
    events = Event.objects.select_related('category').all()
    page_obj = get_pagination(request, events)
    context = {
        "page_obj": page_obj,
    }

    return render(request, 'events/index.html', context)


def event_detail(request, event_id):
    """Отображает выбранный пост."""
    event = get_object_or_404(Event, pk=event_id)
    comments = event.comments.all()
    form = CommentForm()
    context = {
        'event': event,
        'comments': comments,
        'form': form,
    }

    return render(request, 'events/event_detail.html', context)


@login_required
def event_edit(request, event_id):
    """Редактирование выбранного поста."""
    event = get_object_or_404(Event, pk=event_id)
    if event.organizer != request.user:

        return redirect('posts:post_detail', event.pk)

    form = EventForm(
        request.POST or None,
        files=request.FILES or None,
        instance=event
    )
    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect('events:event_detail', event.pk)

    context = {'form': form,
               'is_edit': True,
               'event': event}

    return render(request, 'events/create_event.html', context)


@login_required
def event_create(request):
    """Отображает форму для создания новой записи."""
    form = EventForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.organizer = request.user
        new_post.save()

        return redirect('events:profile', request.user.username)

    return render(request, 'events/create_event.html', {'form': form})


def category_events(request, slug):
    """Отображает все посты выбранной категории в порядке убывания по дате."""
    category = get_object_or_404(Category, slug=slug)
    events = category.events.all()
    page_obj = get_pagination(request, events)
    context = {
        'category': category,
        "page_obj": page_obj,
    }

    return render(request, 'events/category_list.html', context)


def profile(request, username):
    """Отображает профиль зарегистрированного пользователя."""
    author = get_object_or_404(User, username=username)
    events = author.events.all()
    page_obj = get_pagination(request, events)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            author=author, user=request.user
        ).exists()
        context['following'] = following

    return render(request, 'events/profile.html', context)


@login_required
def profile_follow(request, username):
    """Подписка на интересного и забавного автора."""
    author = get_object_or_404(User, username=username)
    if request.user != author and not Follow.objects.filter(
        author=author, user=request.user
    ).exists():
        Follow.objects.create(user=request.user, author=author)

    return redirect('events:profile', author.username)


@login_required
def profile_unfollow(request, username):
    """Отписка от надоеливого или скучного автора."""
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()

    return redirect('events:profile', author.username)


@login_required
def follow_index(request):
    """Отображает посты авторов из подписок пользователя."""
    events = Event.objects.filter(organizer__following__user=request.user)
    page_obj = get_pagination(request, events)
    context = {
        'page_obj': page_obj
    }

    return render(request, 'events/follow.html', context)


@login_required
def add_comment(request, event_id):
    """Написание комметариев к постам."""
    event = get_object_or_404(Event, pk=event_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.event = event
        comment.save()

    return redirect('events:event_detail', event_id=event_id)
