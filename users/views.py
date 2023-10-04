from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')

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