from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
def register(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        
        return render(request, 'register.html')
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')

        if repeat_username(username):
            messages.add_message(
                request, 
                constants.ERROR, 
                f"The username {username} already exists!"
            )
            return redirect('/users/register')
        
        if password != confirm_password:
            messages.add_message(
                request, 
                constants.ERROR, 
                "The passwords don't equals!"
            )
            return redirect('/users/register')
        
        if len(password) < 6:
            messages.add_message(
                request, 
                constants.ERROR, 
                "Your passwords must be longer than 6 digits!"
            )
            return redirect('/users/register')
        
        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            messages.add_message(
                request, 
                constants.SUCCESS, 
                "Account registered!"
            )
        except:
            messages.add_message(
                request, 
                constants.ERROR, 
                "Error in our system!"
            )
            return redirect('/users/register')
        
        return redirect('/users/register')

def repeat_username(user_register):
    try:
        user = User.objects.get(
            username=user_register
        )
        return True
    except:
        return False

def log_in(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        
        return render(request, 'login.html')
    
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            # login
            login(request, user)
            return redirect("/")
        else:
            # warning
            messages.add_message(
                request, 
                constants.ERROR, 
                f"Invalid credentials!"
            )
            return redirect('/users/login')