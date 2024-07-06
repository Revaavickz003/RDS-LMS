from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from frontend.models import Lead
from datetime import datetime, timedelta, date

@login_required(login_url='/login')
def thismonthleads(request):
    current_date = datetime.now()
    this_month_leads = Lead.objects.filter(created_date__year=current_date.year, created_date__month=current_date.month)
    context = {
        "leads": "activete",
        'thismonthleads': True,
        'All_Leads': this_month_leads,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)

@login_required(login_url='/login')
def last30days(request):
    last_30_days_leads = Lead.objects.filter(created_date__gte=datetime.now() - timedelta(days=30))
    context = {
        "leads": "activete",
        'last30days': True,
        'All_Leads': last_30_days_leads,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)

@login_required(login_url='/login')
def prospective_leads(request):
    current_date = datetime.now()
    # Determine the start and end of the financial year
    if current_date.month >= 4:  # April or later
        fiscal_year_start = date(current_date.year, 4, 1)
        fiscal_year_end = date(current_date.year + 1, 3, 31)
    else:  # Before April
        fiscal_year_start = date(current_date.year - 1, 4, 1)
        fiscal_year_end = date(current_date.year, 3, 31)
    
    # Filter leads within the financial year
    fiscal_year_leads = Lead.objects.filter(
        created_date__gte=fiscal_year_start,
        created_date__lte=fiscal_year_end
    )
    prospective_leads = fiscal_year_leads.filter(status__in=['Fresh', 'Follow up', 'Proposed', 'Hold', 'Closed'])
    context = {
        "leads": "activete",
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
        "leads": "activete",
        'monthly_prospective': True,
        'All_Leads': future_prospective_leads,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)

@login_required(login_url='/login')
def last_30_days_prospective(request):
    last_30_days_leads = Lead.objects.filter(created_date__gte=datetime.now() - timedelta(days=30))
    last_30_days_prospective = last_30_days_leads.filter(status__in=['Fresh', 'Follow up', 'Proposed', 'Hold', 'Closed'])
    context = {
        "leads": "activete",
        'last_30_days_prospective': True,
        'All_Leads': last_30_days_prospective,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)

@login_required(login_url='/login')
def span_leads(request):
    span_leads_count = Lead.objects.filter(status__in=['Closed', 'Not Interested' 'Do Not Disturb'])
    context = {
        "leads": "activete",
        'Span_Leads': True,
        'All_Leads': span_leads_count,
    }
    return render(request, 'Revaa/crm_leads_page.html', context)
