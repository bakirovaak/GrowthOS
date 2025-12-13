from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import WheelOfLife, DailyCheckin
from .forms import WheelOfLifeForm, DailyCheckinForm
from django.utils import timezone

@login_required
def dashboard(request):
    # Колесо
    latest_wheel = WheelOfLife.objects.filter(user=request.user).order_by('-created_at').first()
    wheel_form = WheelOfLifeForm(instance=latest_wheel)

    # Чек-ин на сегодня
    today = timezone.now().date()
    checkin_today = DailyCheckin.objects.filter(user=request.user, date=today).first()
    checkin_form = DailyCheckinForm(instance=checkin_today)

    if request.method == 'POST':
        if 'wheel_submit' in request.POST:
            wheel_form = WheelOfLifeForm(request.POST, instance=latest_wheel)
            if wheel_form.is_valid():
                wheel = wheel_form.save(commit=False)
                wheel.user = request.user
                wheel.save()
                return redirect('dashboard')

        elif 'checkin_submit' in request.POST:
            checkin_form = DailyCheckinForm(request.POST, instance=checkin_today)
            if checkin_form.is_valid():
                checkin = checkin_form.save(commit=False)
                checkin.user = request.user
                checkin.date = today
                checkin.save()
                return redirect('dashboard')

    # Все чек-ины за последние 60 дней (для тепловой карты)
    checkins = DailyCheckin.objects.filter(user=request.user, date__gte=today - timezone.timedelta(days=60))

    return render(request, 'dashboard.html', {
        'wheel_form': wheel_form,
        'checkin_form': checkin_form,
        'latest_wheel': latest_wheel,
        'checkin_today': checkin_today,
        'checkins': checkins,
    })