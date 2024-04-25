from django.shortcuts import render, redirect
from frontend.models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def profile(request,):
    context= {
        "settings":"activete",
        "Teams": Team.objects.all(),
    }
    return render(request, "Revaa/Profile_page.html", context)