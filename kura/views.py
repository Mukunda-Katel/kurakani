from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import ChatMessage
from .forms import ChatMessageForm
import json


def home(request):
    return render(request, 'chat/home.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'chat/register.html')
        
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, 'Account created successfully')
        return redirect('login')
    
    return render(request, 'chat/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat_room')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'chat/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def chat_room(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect('chat_room')
    else:
        form = ChatMessageForm()
    
    messages = ChatMessage.objects.all()[:50]  # Get last 50 messages
    return render(request, 'chat/chat_room.html', {
        'form': form,
        'messages': messages
    })


@login_required
def get_messages(request):
    """API endpoint to get messages for AJAX updates"""
    messages = ChatMessage.objects.all()[:50]
    data = []
    for msg in messages:
        data.append({
            'username': msg.user.username,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%H:%M')
        })
    return JsonResponse({'messages': data})