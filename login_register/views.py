from django.contrib.auth.hashers import make_password, check_password
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

        request.session["showLimitAlert"] = True

        if User.objects.filter(username=username):
            passwordHash = User.objects.filter(username=username)[0].passwordHash
            
            if check_password(password, passwordHash):
                messages.success(request, f"{username} logged in")
                request.session["userId"] = User.objects.filter(username=username).values()[0]["id"]
                print(User.objects.filter(username=username).values()[0]["id"])
                return redirect(home_view)
            else:
                messages.error(request, f"Password is wrong for {username}")
        else:
            messages.error(request, f"{username} does not exist")
    return render(request, 'login.html', context={})
    
def signup_view(request: WSGIRequest):
    if request.method == "POST":
        fullName = request.POST["fullname"]
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        budget = request.POST["budget"]
        profilePicture = request.FILES["profile-picture"]
        
        passwordHash = make_password(password)

        if not User.objects.filter(username=username):
            user = User(fullName=fullName, username=username, passwordHash=passwordHash, email=email, budget=budget, profilePicture=profilePicture)
            user.save()
            messages.success(request, f"{username} has been registered succesfully")

            return redirect(signup_view)
        else:
            messages.warning(request, f"{username} already exists")
    return render(request, 'signup.html', context={})

def reset_password_view(request):
    return render(request, 'reset_password.html', context={})

def logout_view(request: WSGIRequest):
    if "userId" in request.session:
        request.session.flush()
    return redirect(login_view)