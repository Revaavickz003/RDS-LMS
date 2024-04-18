from django.shortcuts import render
import calendar
from datetime import datetime
from django.contrib.auth.decorators import login_required
from frontend.models import EmployeeStatus, Team

@login_required(login_url='/login')
def calendar_view(request, year=None, month=None):
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month
    month_name = calendar.month_name[month]

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    cal = calendar.monthcalendar(year, month)
    today =  datetime.today().date().strftime('%Y-%m-%d')

    formatted_data = []
    for week in cal:
        formatted_week = []
        for day in week:
            if day != 0:
                formatted_date = datetime(year, month, day).strftime('%Y-%m-%d')
                formatted_week.append((day, formatted_date))
            else:
                formatted_week.append((day, ''))  # For empty cells
        formatted_data.append(formatted_week)

    usersatus = EmployeeStatus.objects.filter(employee_id = request.user)

    context = {
        'today':today,
        'Calendar': 'active',
        'year': year,
        'month': month,
        'month_name': month_name,
        'calendar_data': formatted_data,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'formatted_date':formatted_date,
        'usersatus':usersatus,
        "Teams": Team.objects.all(),
    }
    return render(request, 'Revaa/calendar.html', context)
