from django.shortcuts import render, redirect
from frontend.models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_history(request, employeeid, employeename):
    context={
        'Employees':'activete',
        "Teams": Team.objects.all(),
    }
    return render (request,'Revaa/single_employee_details_and_history.html',context)

