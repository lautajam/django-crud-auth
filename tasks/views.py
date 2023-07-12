from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.

# Shows the home page
def home(request):
    return render(request, 'home.html')

# Singup the user
def singup(request):
    if request.method == "GET":
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return HttpResponse('User created successfully')
            except:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'The username already exist'
                })
        else:
            return render(request, 'singup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })
