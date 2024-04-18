from django.shortcuts import  render
from frontend.models import *
from django.contrib.auth.decorators import login_required
import json

@login_required(login_url='/login')
def setting(request):
    Roles = Role.objects.all()
    Departments = Department.objects.all()
    Positions = Position.objects.all()
    Users = CustomUser.objects.all()
    Teams = Team.objects.all()

    context = {
        "Roles": Roles,
        "Departments": Departments,
        "Positions": Positions,
        "Users": Users,
        "Teams":Teams,
    }
    return render(request, 'Revaa/setting_page.html', context)
