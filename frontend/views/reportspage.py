from django.shortcuts import render
from frontend.models import Team
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def reportsview(request, teamname):
    try:
        team_details = Team.objects.get(team_name=teamname)
        
        
        context = {
            'team_details': team_details
        }
        return render(request, 'Revaa/reports.html', context)
    except Team.DoesNotExist:
        return render(request, 'team_not_found.html')
