from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from growth.views import dashboard, export_pdf, register  
urlpatterns = [
    path('admin/', admin.site.urls),

    # Логин и логаут
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Регистрация — добавь эту строку
    path('register/', register, name='register'),

    # Экспорт PDF
    path('export-pdf/', export_pdf, name='export_pdf'),

    # Главная — дашборд
    path('', dashboard, name='dashboard'),
]