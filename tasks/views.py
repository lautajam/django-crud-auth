from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task

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

# Close session
def singout(request):
    logout(request)
    return redirect('home')

# Login the usser
def singin(request):
    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'singin.html', {
                'form': AuthenticationForm,
                'error': "Username or password is incorrect"
            })
        else:
            login(request, user)
            return redirect('tasks')

# Show user tasks
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

#The user can create tasks
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save() 
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': "Please provide valid data "
        })

def task_detail(request,task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {
        'task': task
    })