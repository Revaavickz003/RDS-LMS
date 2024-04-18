from django.shortcuts import  render
from frontend.models import *
import datetime

def task_sheet_function(request, user, date):
    if  request.method == 'POST':
        assigned_to_ids = request.POST.getlist('employees')
        assigned_to = CustomUser.objects.filter(pk__in=assigned_to_ids)
        for employee in assigned_to:
            new_task = TasksheetTable.objects.create(
                date = datetime.datetime.today(),
                client = request.POST['client'],
                types = request.POST['type'],
                task = request.POST['task'],
                expected_time = request.POST['expected_time'],
                assigned_to = employee,
                assigned_by = CustomUser.objects.get(username=user),
                status =  "Assigned",
                remarks = request.POST['remarks']
            )
            new_task.save()
        

    Assigned_By_Report = TasksheetTable.objects.filter(assigned_to=request.user, date=date)
    Assigned_To_Report = TasksheetTable.objects.filter(assigned_by=request.user, date=date)
    

    newdate = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    day_of_week = newdate.strftime('%A')


    context = {
    'date':newdate,
    'day_of_week':day_of_week,
    'Assigned_By_Report': Assigned_By_Report,
    'Assigned_To_Report': Assigned_To_Report,
    'Users': CustomUser.objects.filter(),
    }
    
    return render(request, 'Revaa/tasksheet.html', context)