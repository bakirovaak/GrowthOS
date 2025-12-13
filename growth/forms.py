from django import forms
from .models import WheelOfLife, DailyCheckin

class WheelOfLifeForm(forms.ModelForm):
    class Meta:
        model = WheelOfLife
        fields = '__all__'
        exclude = ['user', 'created_at']

class DailyCheckinForm(forms.ModelForm):
    class Meta:
        model = DailyCheckin
        fields = ['mood', 'energy', 'gratitude']
        widgets = {
            'gratitude': forms.Textarea(attrs={'rows': 3, 'placeholder': 'За что ты сегодня благодарен?'})
        }