from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from better_profanity import profanity
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.exceptions import ValidationError
import calendar

def index(request):
    entries = Entry.objects.filter(verified=True)
    topic = Topic.objects.filter(verified=True)
    topics = topic.order_by('-views')
    context = {"entries" : entries, "topics" : topics}
    return render(request, 'learning_logs/index.html', context)

def topics(request):
    verified = Topic.objects.filter(verified=True)
    topics = verified.order_by("-date_added")
    context = {"topics" : topics}
    return render(request,"learning_logs/topics.html", context)

def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topic.views += 1
    topic.save()
    entry = topic.entry_set.filter(verified=True)
    entries = entry.order_by('-date_added').select_related('author')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    #entry.views += 1
    topic = entry.topic
    user = entry.author
    
    context = {"entry" : entry, "topic" : topic, "user" : user}
    return render(request, "learning_logs/entry.html", context)

def month_filter(request, month):
    dates = Entry.objects.filter(date_added__month=month)
    month_name = calendar.month_name[int(month)]
    context = {'dates' : dates,"month" : month_name}
    return render(request, "learning_logs/date_filter.html", context)

@login_required
def new_topic(request):
    form = TopicForm()
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.author = request.user
            try:
                new_topic.save()  # try to save the entry
            except ValidationError as e:
                # handle validation error by adding error message to form
                form.add_error('text', e.message)
            else:
                return redirect("learning_logs:topics")
    context = {"form" : form}
    return render(request, "learning_logs/new_topic.html", context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    form = EntryForm()
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.author = request.user
            new_entry.verified = True
            try:
                new_entry.save()  # try to save the entry
            except ValidationError as e:
                # handle validation error by adding error message to form
                form.add_error('text', e.message)
            else:
                return redirect("learning_logs:topic", topic_id=topic_id)
    context = {"form" : form, "topic" : topic}
    return render(request, "learning_logs/new_entry.html", context)
@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if entry.author != request.user:
       raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.author = request.user
            new_entry.verified = True
            try:
                new_entry.save()  # try to save the entry
            except ValidationError as e:
                # handle validation error by adding error message to form
                form.add_error('text', e.message)
            else:
                entry.delete()
                return redirect("learning_logs:topic", topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)  
    if entry.author != request.user:
        raise PermissionDenied
    else:
        entry.delete()
    return redirect(request.META.get('HTTP_REFERER'))