from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'login.html', context={})

def signup_view(request):
    return render(request, 'signup.html', context={})

def reset_password_view(request):
    return render(request, 'reset_password.html', context={})