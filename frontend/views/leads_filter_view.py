from datetime import timedelta
from django.shortcuts import render, redirect
from frontend.models import *
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def ledas_filter(request):
    if request.method == 'POST':
        # Retrieve form data
        # company_name = request.POST.getlist('companyname')  # Change to get, assuming it's a single value
        # company_type = request.POST.getlist('companytype')
        # location = request.POST.getlist('Location')
        # city = request.POST.getlist('City')
        # lead_name = request.POST.getlist('leadname')
        # business_type = request.POST.getlist('bussinesstype')
        # product = request.POST.getlist('Product')
        # priority = request.POST.getlist('Priority')
        # status = request.POST.getlist('Status')
        # created_by = request.POST.getlist('Createdby')
        # from_amount = request.POST.get('fromAmount')
        # to_amount = request.POST.get('toamount')

        from_date = request.POST.get('Fromdate')
        to_date = request.POST.get('todate')

        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if to_date:
            to_date = to_date + timedelta(days=1)
        
        leads = Lead.objects.all()
        
        # if company_name:
        #     leads = leads.filter(org_name__in=company_name)  # Using icontains for case-insensitive search
        # if company_type:
        #     leads = leads.filter(org_type__in=company_type)
        # if location:
        #     leads = leads.filter(location__in=location)
        # if city:
        #     leads = leads.filter(city__in=city)
        # if lead_name:
        #     leads = leads.filter(lead_name__in=lead_name)
        # if business_type:
        #     leads = leads.filter(business_type__in=business_type)
        # if product:
        #     leads = leads.filter(products__in=product)
        # if priority:
        #     leads = leads.filter(priority__in=priority)
        # if status:
        #     leads = leads.filter(status__in=status)
        # if created_by:
        #     leads = leads.filter(created_by__in=created_by)
        # if from_amount:
        #     leads = leads.filter(amount__gte=from_amount)
        # if to_amount:
        #     leads = leads.filter(amount__lte=to_amount)
        if from_date and to_date:
            leads = leads.filter(created_date__gte=from_date, created_date__lt=to_date)
        elif from_date:
            leads = leads.filter(created_date__gte=from_date)
        elif to_date:
            leads = leads.filter(created_date__lt=to_date)

        context = {
            "leads": "activete",
            'All_Leads': leads,
            # "Teams": Team.objects.all(),
            # "Org_Type": OrgType.objects.all(),
            # "Locations": Location.objects.all(),
            # "citys": City.objects.all(),
            # "lead_names": LeadTable.objects.all(),
            # "BUSINESS_TYPE_CHOICES": Lead.BUSINESS_TYPE_CHOICES,
            # "Products": ProductTable.objects.all(),
            # "Prioritys": Lead.PRIORITY_CHOICES,
            # "Statuss": Lead.STATUS_CHOICES,
            "users": CustomUser.objects.filter(is_admin=True, is_active=True),
            
        }
        return render(request, 'Revaa/crm_leads_page.html', context)
    else:
        # Handle GET request
        context = {
            'leads': Lead.objects.all(),
            'title': 'Leads Filter'
        }
        return redirect('leads')
