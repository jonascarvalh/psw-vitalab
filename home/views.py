from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(
            request, 
            'home.html', 
            {
                'authenticated': 'True',
                'is_staff': request.user.is_staff
            }
        )
    
    return render(request, 'home.html')
    