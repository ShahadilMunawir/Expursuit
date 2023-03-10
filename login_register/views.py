from django.shortcuts import render, HttpResponse, redirect
from django.core.handlers.wsgi import WSGIRequest
from login_register.models import User
from django.contrib import messages
from home.views import home_view

# Create your views here.

def login_view(request: WSGIRequest):
    if "userId" in request.session:
        return redirect(home_view)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username, password=password):
            messages.success(request, f"{username} logged in")
            request.session["userId"] = User.objects.filter(username=username).values()[0]["id"]
            print(User.objects.filter(username=username).values()[0]["id"])
            return redirect(home_view)
        else:
            messages.error(request, f"{username} not found or wrong password")
    return render(request, 'login.html', context={})
    
def signup_view(request: WSGIRequest):
    if request.method == "POST":
        fullname = request.POST["fullname"]
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        budget = request.POST["budget"]
        profilePicture = request.FILES["profile-picture"]
        
        if not User.objects.filter(username=username):
            user = User(fullname=fullname, username=username, password=password, email=email, budget=budget, profilePicture=profilePicture)
            user.save()
            messages.success(request, f"{username} has been registered succesfully")
        else:
            messages.warning(request, f"{username} already exists")
    return render(request, 'signup.html', context={})

def reset_password_view(request):
    return render(request, 'reset_password.html', context={})

def logout_view(request: WSGIRequest):
    if "userId" in request.session:
        request.session.flush()
    return redirect(login_view)