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
                'user': request.user
            }
        )
    
    return render(request, 'home.html')
    