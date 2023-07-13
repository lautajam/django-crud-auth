from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .models import Task

# Render the template 'home.html'.
def home(request):
    return render(request, 'home.html')

# Create the user and check if it already exists
def signup(request):
    # If the request is GET, render the template 'signup.html' with the form UserCreationForm
    # If request is POST, checks if passwords match and creates a new user
    # In case of errors, displays error messages in the template 'signup.html'.
    if request.method == "GET":
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(
                        username=request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('tasks')
                except IntegrityError:
                    return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': 'User already exist'
                    })
            else:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Password do not match'
                })
        except ValueError:
            return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': 'Complete data'
                    })

# Close session
@login_required
def signout(request):
    logout(request)
    return redirect('home')

# Login the usser
def signin(request):
    # If the request is GET, renders the template 'signin.html' with the AuthenticationForm form
    # If request is POST, verifies login credentials and authenticates the user
    # In case of incorrect credentials, displays an error message in the template 'signin.html'.
    # In case of correct credentials, logs the user in and redirects to the tasks page.
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "Username or password is incorrect"
            })
        else:
            login(request, user)
            return redirect('tasks')

# Retrieves the current user's tasks that have not yet been completed.
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

# Create a task
@login_required
def create_task(request):
    # If the request is GET, renders the template 'create_task.html' with the TaskForm form
    # If the request is POST, it saves a new task with the data provided by the form.
    # In case of errors, displays an error message in the template 'create_task.html'.
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

# Shows the details about a task request
@login_required
def task_detail(request,task_id):
    # If the request is GET, obtains the task corresponding to the task_id and renders the template 'task_detail.html' with the TaskForm form
    # If the request is POST, it updates the task with the data provided by the form.
    # In case of errors, it displays an error message in the template 'task_detail.html'.
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'form': form,
            'task_id': task_id
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save() 
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'form': TaskForm,
            'error': "Error updating task"
        })

# Complete the task request
@login_required
def complete_task(request, task_id):
    # Gets the task corresponding to the task_id and marks the date of completion if the request is POSTed
    # Redirects the user to the tasks page after task completion
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now() 
        task.save()
        return redirect('tasks')

# Delete the task request
@login_required
def delete_task(request, task_id):
    # Gets the task corresponding to the task_id and deletes it if the request is a POST request
    # Redirects the user to the tasks page after deleting the task
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
# Show user tasks completed
@login_required
def tasks_completed(request):
    # Retrieves the current user's completed tasks sorted by date of completion in descending order.
    # Renders the 'tasks.html' template with the retrieved tasks
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })