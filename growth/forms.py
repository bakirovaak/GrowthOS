from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import WheelOfLife, DailyCheckin, Habit

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class WheelOfLifeForm(forms.ModelForm):
    class Meta:
        model = WheelOfLife
        exclude = ['user', 'created_at']  # все поля кроме user и даты

class DailyCheckinForm(forms.ModelForm):
    class Meta:
        model = DailyCheckin
        exclude = ['user', 'date']
        widgets = {
            'gratitude': forms.Textarea(attrs={'rows': 4, 'placeholder': 'За что ты благодарна сегодня?'})
        }

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'target_days', 'sphere']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название привычки'}),
            'target_days': forms.NumberInput(attrs={'min': 1, 'max': 7, 'value': 7}),
            'sphere': forms.TextInput(attrs={'placeholder': 'Сфера (например, Здоровье)'}),
        }
