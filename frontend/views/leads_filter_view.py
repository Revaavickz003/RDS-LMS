from datetime import timedelta
from django.shortcuts import render, redirect
from frontend.models import *
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def ledas_filter(request):
    if request.method == 'POST':
        from_date = request.POST.get('Fromdate')
        to_date = request.POST.get('todate')

        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if to_date:
            to_date = to_date + timedelta(days=1)
        
        leads = Lead.objects.all()
        
        if from_date and to_date:
            leads = leads.filter(created_date__gte=from_date, created_date__lt=to_date)
        elif from_date:
            leads = leads.filter(created_date__gte=from_date)
        elif to_date:
            leads = leads.filter(created_date__lt=to_date)

        context = {
            "leads": "activete",
            'All_Leads': leads,
        }
        return render(request, 'Revaa/crm_leads_page.html', context)
    else:
        return redirect("coustomer")
