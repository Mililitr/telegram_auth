# telegram_auth/urls.py
from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('profile/', views.profile, name='profile'),
    path('generate-telegram-link/', views.generate_telegram_link, name='generate_telegram_link'),
    path('check-auth/', views.check_auth, name='check_auth'),
]