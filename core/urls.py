from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from growth.views import dashboard  # ← оставляем только dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # Авторизация (встроенная в Django)
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Главная страница — наш дашборд
    path('', dashboard, name='dashboard'),
]