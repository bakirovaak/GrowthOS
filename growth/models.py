from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class WheelOfLife(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # 12 сфер жизни
    health = models.IntegerField(default=5)           # здоровье и энергия
    emotions = models.IntegerField(default=5)         # эмоции
    relationships = models.IntegerField(default=5)    # отношения
    family = models.IntegerField(default=5)
    personal_growth = models.IntegerField(default=5)
    finances = models.IntegerField(default=5)
    career_study = models.IntegerField(default=5)
    rest_hobby = models.IntegerField(default=5)
    environment = models.IntegerField(default=5)
    spirituality = models.IntegerField(default=5)
    creativity = models.IntegerField(default=5)
    contribution = models.IntegerField(default=5)

    class Meta:
        verbose_name = "Колесо баланса жизни"
        ordering = ['-created_at']

    def __str__(self):
        return f"Колесо {self.user.username} от {self.created_at.strftime('%d.%m.%Y')}"
    
    from django.utils import timezone
from datetime import date

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