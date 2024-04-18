from django.shortcuts import render, redirect
from django.contrib import messages
from frontend.models import Team, CustomUser, Department
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def addteams(request):
    if request.method == 'POST':
        team_name = request.POST['teamName']
        team_icon = request.FILES['teamIcon']
        department_id = request.POST['deportment_selected']
        employees_ids = request.POST.getlist('employees')
        employees = CustomUser.objects.filter(id__in=employees_ids)
        department = Department.objects.get(id=department_id)
        
        if not Team.objects.filter(team_name=team_name) and len(team_name) < 50:
            new_team = Team.objects.create(
                team_name=team_name, 
                team_icon=team_icon, 
                deportment=department,
                created_by =request.user,
            )
            new_team.members.set(employees)  
            new_team.save()
            messages.success(request, "New Team Added Successfully!")
            return redirect('setting')
        else:
            messages.error(request, f"{team_name} is allready added ...")
            return redirect('setting')
    else:
        messages.error(request, "Error Occurred while Adding the Team.")
        return redirect('setting')
