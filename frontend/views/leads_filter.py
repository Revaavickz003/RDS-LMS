from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from frontend.models import Lead
from datetime import datetime, timedelta

@login_required(login_url='/login')
def thismonthleads(request):
    current_date = datetime.now()
    this_month_leads = Lead.objects.filter(created_date__year=current_date.year, created_date__month=current_date.month)
    context = {
        "leads": "active",
        'thismonthleads': True,
        'All_Leads': this_month_leads,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)

@login_required(login_url='/login')
def last30days(request):
    last_30_days_leads = Lead.objects.filter(created_date__gte=datetime.now() - timedelta(days=30))
    context = {
        "leads": "active",
        'last30days': True,
        'All_Leads': last_30_days_leads,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)

@login_required(login_url='/login')
def prospective_leads(request):
    prospective_leads = Lead.objects.filter(status__in=['Fresh', 'Follow up', 'Proposed', 'Hold', 'Closed'])
    context = {
        "leads": "active",
        'prospective_leads': True,
        'All_Leads': prospective_leads,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)

@login_required(login_url='/login')
def monthly_prospective(request):
    current_date = datetime.now()
    this_month_leads = Lead.objects.filter(created_date__year=current_date.year, created_date__month=current_date.month)
    future_prospective_leads = this_month_leads.filter(status__in=['Fresh', 'Follow up', 'Proposed', 'Hold', 'Closed'])
    context = {
        "leads": "active",
        'monthly_prospective': True,
        'All_Leads': future_prospective_leads,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)

@login_required(login_url='/login')
def last_30_days_prospective(request):
    last_30_days_leads = Lead.objects.filter(created_date__gte=datetime.now() - timedelta(days=30))
    last_30_days_prospective = last_30_days_leads.filter(status__in=['Fresh', 'Follow up', 'Proposed', 'Hold', 'Closed'])
    context = {
        "leads": "active",
        'last_30_days_prospective': True,
        'All_Leads': last_30_days_prospective,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)

@login_required(login_url='/login')
def span_leads(request):
    span_leads_count = Lead.objects.filter(status__in=['Closed', 'Not Interested', 'Do Not Disturb'])
    context = {
        "leads": "active",
        'Span_Leads': True,
        'All_Leads': span_leads_count,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)
