from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

# Shows the home page
def home(request):
    return render(request, 'home.html')

# Create the user and check if it already exists
def singup(request):
    if request.method == "GET":
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks') 
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exist'
                })
        else:
            return render(request, 'singup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })

def tasks(request):
    return render(request, 'tasks.html')