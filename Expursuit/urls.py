"""Expursuit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from index.views import root_view
from login_register.views import login_view, signup_view, reset_password_view, home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_view),
    path('home/', home_view),
    path('login/', login_view),
    path('signup/', signup_view),
    path('reset_password', reset_password_view),
]
