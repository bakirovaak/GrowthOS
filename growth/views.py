from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.utils import timezone
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def wheel_detail(request):
    wheel = WheelOfLife.objects.filter(user=request.user).order_by('-created_at').first()
    
    return render(request, 'wheel_detail.html', {
        'wheel': wheel,
    })
# Регистрация
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# Логин
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    today = timezone.now().date()

    # Колесо баланса 
    latest_wheel = WheelOfLife.objects.filter(user=request.user).order_by('-created_at').first()
    wheel_form = WheelOfLifeForm(instance=latest_wheel)

    # Чекин сегодня
    checkin_today = DailyCheckin.objects.filter(user=request.user, date=today).first()
    checkin_form = DailyCheckinForm(instance=checkin_today)

    # Привычки
    habits = Habit.objects.filter(user=request.user)
    habit_form = HabitForm()


    # crud
    if request.method == 'POST':
        if 'wheel_submit' in request.POST:
            wheel_form = WheelOfLifeForm(request.POST, instance=latest_wheel)
            if wheel_form.is_valid():
                wheel = wheel_form.save(commit=False)
                wheel.user = request.user
                wheel.save()
                return redirect('dashboard')
            
            # update

        elif 'checkin_submit' in request.POST:
            checkin_form = DailyCheckinForm(request.POST, instance=checkin_today)
            if checkin_form.is_valid():
                checkin = checkin_form.save(commit=False)
                checkin.user = request.user
                checkin.date = today
                checkin.save()
                return redirect('dashboard')
            
      #Добавление привычки
        elif 'habit_add' in request.POST:
            habit_form = HabitForm(request.POST)
            if habit_form.is_valid():
                habit = habit_form.save(commit=False)
                habit.user = request.user
                habit.save()
                return redirect('dashboard')

        elif 'habit_delete' in request.POST:
            habit_id = request.POST.get('habit_id')
            habit = get_object_or_404(Habit, id=habit_id, user=request.user)
            habit.delete()
            return redirect('dashboard')

    # Последние 30 чек-инов для календаря настроения
    checkins = DailyCheckin.objects.filter(user=request.user).order_by('-date')[:30]

    return render(request, 'dashboard.html', {
        'wheel_form': wheel_form,
        'checkin_form': checkin_form,
        'habit_form': habit_form,
        'latest_wheel': latest_wheel,        # для радара и отображения
        'checkin_today': checkin_today,      # для чек-ина сегодня
        'habits': habits,                    #трекера привычек
        'checkins': checkins,                #настроения
        'today': today,
    })

# Экспорт PDF
@login_required
def export_pdf(request):
    latest_wheel = WheelOfLife.objects.filter(user=request.user).order_by('-created_at').first()
    checkins = DailyCheckin.objects.filter(user=request.user).order_by('-date')[:30]

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 2 * cm, "GrowthOS — Отчёт о личностном росте")

    p.setFont("Helvetica", 14)
    p.drawString(2 * cm, height - 4 * cm, f"Пользователь: {request.user.username}")
    p.drawString(2 * cm, height - 5 * cm, f"Дата: {timezone.now().strftime('%d.%m.%Y')}")

    y = height - 7 * cm

    p.setFont("Helvetica-Bold", 18)
    p.drawString(2 * cm, y, "Колесо баланса жизни")
    y -= cm

    p.setFont("Helvetica", 14)
    if latest_wheel:
        spheres = [
            ("Здоровье и энергия", latest_wheel.health),
            ("Эмоции и настроение", latest_wheel.emotions),
            ("Отношения и любовь", latest_wheel.relationships),
            ("Семья и друзья", latest_wheel.family),
            ("Личностный рост", latest_wheel.personal_growth),
            ("Финансы", latest_wheel.finances),
            ("Карьера / учёба", latest_wheel.career_study),
            ("Отдых и хобби", latest_wheel.rest_hobby),
            ("Окружение и быт", latest_wheel.environment),
            ("Духовность и смысл", latest_wheel.spirituality),
            ("Творчество", latest_wheel.creativity),
            ("Вклад в мир", latest_wheel.contribution),
        ]
        for name, value in spheres:
            p.drawString(3 * cm, y, f"{name}: {value}/10")
            y -= 0.8 * cm
    else:
        p.drawString(3 * cm, y, "Колесо баланса ещё не заполнено.")
    y -= 2 * cm

    p.setFont("Helvetica-Bold", 18)
    p.drawString(2 * cm, y, "Ежедневные чек-ины (последние 30 дней)")
    y -= cm

    p.setFont("Helvetica", 12)
    p.drawString(2 * cm, y, "Дата        Настроение    Энергия    Благодарность")
    y -= 0.8 * cm
    p.drawString(2 * cm, y, "-------------------------------------------------------------")
    y -= 0.8 * cm

    for checkin in checkins:
        gratitude = checkin.gratitude or "—"
        line = f"{checkin.date.strftime('%d.%m.%Y')}      {checkin.mood}/10         {checkin.energy}/10       {gratitude[:40]}"
        p.drawString(2 * cm, y, line)
        y -= 0.8 * cm

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="GrowthOS_report.pdf"'
    return response