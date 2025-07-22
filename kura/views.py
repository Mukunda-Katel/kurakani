from django.shortcuts import render
from django.contrib.auth.models import User
from 

# Create your views here.
def home(request):
    return render(request, '')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exist")
            return render(request, '')
        
        
            
        
        
    