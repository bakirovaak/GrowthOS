from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class WheelOfLife(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # 12 сфер жизни
    Здоровье = models.IntegerField(default=5)           
    Удовлетворенность = models.IntegerField(default=5)        
    Отношения = models.IntegerField(default=5)    
    Семья = models.IntegerField(default=5)
    Личностныйрост = models.IntegerField(default=5)
    Финанасы = models.IntegerField(default=5)
    Учеба = models.IntegerField(default=5)
    Хобби= models.IntegerField(default=5)
    Друзья = models.IntegerField(default=5)
    Уровень_счатья = models.IntegerField(default=5)
    Чтение = models.IntegerField(default=5)
    Волонтёрство = models.IntegerField(default=5)

    class Meta:
        verbose_name = "Колесо баланса жизни"
        ordering = ['-created_at']

    def __str__(self):
        return f"Колесо {self.user.username} от {self.created_at.strftime('%d.%m.%Y')}"


class DailyCheckin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    mood = models.IntegerField()          # 1–10
    energy = models.IntegerField()        # 1–10
    gratitude = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} — {self.date} — настроение {self.mood}"


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # название привычки
    target_days = models.PositiveIntegerField(default=7)  # сколько раз в неделю
    sphere = models.CharField(max_length=100, blank=True)  # связь с колесом, например "Здоровье"
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)  # для сортировки

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name