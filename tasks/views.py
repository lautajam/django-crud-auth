from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def helloworld(request):
    title = "Hello world"
    return render(request, 'singup.html', {
        'form': UserCreationForm
    })