import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from frontend.models import Lead, OrgType, Location, City, LeadTable, ProductTable, OrgName, CustomUser, UserActivity
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from datetime import date, datetime

@login_required(login_url='/login')
def crm_page_view(request):
    if request.method == 'POST':
        client_name = request.POST.get('Client_name', '')
        client_number = request.POST.get('Client_number', '')
        company_name = request.POST.get('Company_name', '')
        company_type = request.POST.get('Company_type', '')
        country = request.POST.get('Country', '')
        city = request.POST.get('city', '')
        reffral_name = request.POST.get('lead_name', '')
        business_type = request.POST.get('bussinesstype', '')
        proposal_amount = request.POST.get('Amount', '')
        finally_budjet = request.POST.get('Amount', '')
        end_of_date = request.POST.get('enddate', '')
        priority = request.POST.get('Prioritys', '')
        mail_id = request.POST.get('email', '')
        status = request.POST.get('satus', '')
        additional_remarks = request.POST.get('comments', '')
        call_back_comments = request.POST.get('Remarks', '')
        call_back = request.POST.get('callbackdate', '')

        # Check for missing required fields and add error messages
        if not client_name:
            messages.error(request, "Client name is required.")
        if not client_number:
            messages.error(request, "Client number is required.")
        if not company_name:
            messages.error(request, "Company name is required.")
        if not company_type:
            messages.error(request, "Company type is required.")
        else:
            company_type = OrgType.objects.get(pk = company_type)
        if not country:
            messages.error(request, "Country is required.")
        else:
            country = Location.objects.get(location = country)
        if not city:
            messages.error(request, "City is required.")
        else:
            city = City.objects.get(city = city)
        if not reffral_name:
            messages.error(request, "Referral name is required.")
        else:
            reffral_name = LeadTable.objects.get(Lead_Name = reffral_name)
        if not business_type:
            messages.error(request, "Business type is required.")
        if not proposal_amount:
            messages.error(request, "Proposal amount is required.")
        if not finally_budjet:
            finally_budjet = proposal_amount
        if not end_of_date:
            messages.error(request, "End date is required.")
        if not priority:
            messages.error(request, "Priority is required.")
        if not mail_id:
            mail_id = None
        if not status:
            messages.error(request, "Status is required.")
        if not additional_remarks:
            messages.error(request, "Additional remarks are required.")
        if not call_back_comments:
            messages.error(request, "Call back comments are required.")
        if not call_back:
            messages.error(request, "Call back date is required.")

        try:
            selected_product_names = request.POST.getlist('products')
        except:
            return render(request, 'Revaa/crm_template.html', {'error': 'Invalid lead'})

        try:
            new_lead = Lead.objects.create(
                client_name=client_name,
                client_number=client_number,
                company_name=company_name,
                company_type=company_type,
                country=country,
                city=city,
                reffral_name=reffral_name,
                business_type=business_type,
                proposal_amount=proposal_amount,
                finally_budjet=finally_budjet,
                end_of_date=end_of_date,
                priority=priority,
                mail_id=mail_id,
                status=status,
                additional_remarks=additional_remarks,
                call_back_comments=call_back_comments,
                call_back=call_back,
                created_by = request.user,
                created_date = datetime.now(),
                updated_by = request.user,
                updated_date = datetime.now(),
            )

            selected_products = ProductTable.objects.filter(Product_Name__in=selected_product_names)
            new_lead.products.set(selected_products)

            new_lead.save()
    
            UserActivity.objects.create(
                user=request.user,
                timestamp=timezone.now(),
                lable = f"Create Lead, {new_lead.client_name}, {new_lead.company_name} company",
                action="Created",
                content_type=ContentType.objects.get_for_model(Lead),
                object_id=new_lead.pk,
            )
            return redirect('leads')
        except Exception as e:
            messages.error(request, f"{e}")
            return redirect('leads')
        
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
    context = {
        "leads": "activete",
        'leadslistpage':True,
        'All_Leads': fiscal_year_leads,
        "Org_Type": OrgType.objects.all(),
        "Locations": Location.objects.all(),
        "citys": City.objects.all(),
        "BUSINESS_TYPE_CHOICES": Lead.BUSINESS_TYPE_CHOICES,
        "STATUS_CHOICES": Lead.STATUS_CHOICES,
        "PRIORITY_CHOICES": Lead.PRIORITY_CHOICES,
        "ref_names":LeadTable.objects.all(),
        "Products": ProductTable.objects.all(),
        "users": CustomUser.objects.filter(is_admin=True, is_active=True),
    }

    return render(request, 'Revaa/crm_leads_page.html', context)


@login_required(login_url='/login')
def without_view(request):
    context = {
        "leads": "activete",
        'leadspage':'leadspage',
        'All_Leads': Lead.objects.filter(is_customer=False),
        "Org_Type": OrgType.objects.all(),
        "Locations": Location.objects.all(),
        "citys": City.objects.all(),
        "lead_names": LeadTable.objects.all(),
        "BUSINESS_TYPE_CHOICES": Lead.BUSINESS_TYPE_CHOICES,
        "Products": ProductTable.objects.all(),
        "Prioritys": Lead.PRIORITY_CHOICES,
        "Statuss": Lead.STATUS_CHOICES,
        'Org_Name': OrgName.objects.all(),
        "users": CustomUser.objects.exclude(is_admin=True, is_active=True),
    }

    return render(request, 'Revaa/crm_leads_page.html', context)