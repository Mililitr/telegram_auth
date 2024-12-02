# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import TelegramUser
import uuid
import json

def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'accounts/login.html')

def generate_telegram_link(request):
    token = str(uuid.uuid4())
    request.session['auth_token'] = token
    bot_username = 'telegtestwebbot_bot'
    telegram_link = f'https://t.me/{bot_username}?start={token}'
    return JsonResponse({'link': telegram_link})

def check_auth(request):
    token = request.session.get('auth_token')
    if token:
        try:
            telegram_user = TelegramUser.objects.get(auth_token=token)
            if not telegram_user.user:
                # Create new user if doesn't exist
                user = User.objects.create_user(username=telegram_user.telegram_username)
                telegram_user.user = user
                telegram_user.save()
            login(request, telegram_user.user)
            return JsonResponse({'authenticated': True, 'username': telegram_user.telegram_username})
        except TelegramUser.DoesNotExist:
            pass
    return JsonResponse({'authenticated': False})

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/profile.html')