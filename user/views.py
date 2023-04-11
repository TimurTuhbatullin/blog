from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from learning_logs.models import Entry
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('learning_logs:home')
    context = {"form" : form}
    return render(request, 'registration/register.html', context)
        

def profile(request, user_id):
    user = User.objects.get(id=user_id)
    entries = Entry.objects.filter(author = user, verified = True)
    context = {'user' : user,  'entries': entries}
    return render(request, 'registration/profile.html', context)

def log_out(request):
    logout(request)
    return redirect("learning_logs:home")