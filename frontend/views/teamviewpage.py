from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from frontend.models import *

@login_required(login_url='/login')
def teamview(request, teamname):
    try:
        team_details = Team.objects.get(team_name=teamname)
        team_members = CustomUser.objects.filter(teams=team_details)
        context = {
            'active_team_name': teamname,
            "Teams": Team.objects.all(),
            'team_details': team_details,
            'team_members':team_members,
        }
    except Exception as e:
        print(e)
        
    return render(request, 'Revaa/teampage.html',context)