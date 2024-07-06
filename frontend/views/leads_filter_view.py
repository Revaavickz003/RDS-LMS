from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from frontend.models import *
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from datetime import date, datetime

@login_required(login_url='/login')
def leads_filter(request):
    if request.method == 'POST':
        from_date = request.POST.get('Fromdate')
        to_date = request.POST.get('todate')
        orgtype = request.POST.get('Org_Type')
        country = request.POST.get('country')
        city = request.POST.get('City')
        business_type = request.POST.get('Business')
        services = request.POST.get('Services') 

        # Parse dates
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if to_date:
            to_date += timedelta(days=1)

        current_date = datetime.now()
        # Determine the start and end of the financial year
        if current_date.month >= 4:  # April or later
            fiscal_year_start = date(current_date.year, 4, 1)
            fiscal_year_end = date(current_date.year + 1, 3, 31)
        else:  # Before April
            fiscal_year_start = date(current_date.year - 1, 4, 1)
            fiscal_year_end = date(current_date.year, 3, 31)
        
        leads = Lead.objects.filter(
            created_date__gte=fiscal_year_start,
            created_date__lte=fiscal_year_end
    )

        # Apply filters
        if from_date and to_date:
            leads = leads.filter(created_date__gte=from_date, created_date__lt=to_date)
        if orgtype:
            leads = leads.filter(company_type__org_type=orgtype)
        if country:
            leads = leads.filter(country__location=country)
        if city:
            leads = leads.filter(city__city=city)
        if business_type:
            leads = leads.filter(business_type=business_type)
        if services:
            leads = leads.filter(products__Product_Name__in=services).distinct()

        context = {
            "leads": "activete",
            'Fiter_page': True,
            'All_Leads': leads,
            "Org_Type": OrgType.objects.all(),
            "Locations": Location.objects.all(),
            "citys": City.objects.all(),
            "lead_names": LeadTable.objects.all(),
            "BUSINESS_TYPE_CHOICES": Lead.BUSINESS_TYPE_CHOICES,
            "Products": ProductTable.objects.all(),
            "users": CustomUser.objects.exclude(is_admin=True, is_active=True),
        }
        return render(request, 'Revaa/crm_leads_page.html', context)
    else:
        return redirect("customer")
