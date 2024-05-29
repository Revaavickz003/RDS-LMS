import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from frontend.models import Lead, OrgType, Location, City, LeadTable, ProductTable, Team, OrgName, CustomUser, UserActivity
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

@login_required(login_url='/login')
def crm_page_view(request):
    if request.method == 'POST':
        client_name=request.POST['Client_name'],
        client_number=request.POST['Client_number'],
        company_name=request.POST['Company_name'],
        company_type=request.POST['Company_type'],
        country=request.POST['Country'],
        city=request.POST['city'],
        reffral_name=request.POST['lead_name'],
        business_type=request.POST['bussinesstype'],
        proposal_amount=request.POST['Amount'],
        finally_budjet=request.POST['Amount'],
        end_of_date=request.POST['enddate'],
        priority=request.POST['Prioritys'],
        mail_id=request.POST['email'],
        status=request.POST['satus'],
        additional_remarks=request.POST['comments'],
        call_back_comments=request.POST['Remarks'],
        call_back=request.POST['callbackdate'],

        print(client_name)
        print(client_number)
        print(company_name)
        print(company_type)
        print(country)
        print(city)
        print(reffral_name)
        print(business_type)
        print(proposal_amount)
        print(finally_budjet)
        print(end_of_date)
        print(priority)
        print(mail_id)
        print(status)
        print(additional_remarks)
        print(call_back_comments)
        print(call_back)

        try:
            selected_product_names = request.POST.getlist('products')
        except:
            return render(request, 'Revaa/crm_template.html', {'error': 'Invalid lead'})

        # try:
        #     new_lead = Lead.objects.create(
        #         client_name=request.POST['Client_name'],
        #         client_number=request.POST['Client_number'],
        #         company_name=request.POST['Company_name'],
        #         company_type=Create_Company_type,
        #         country=Locations,
        #         city=city_name,
        #         reffral_name=lead_name,
        #         business_type=request.POST['bussinesstype'],
        #         proposal_amount=request.POST['Amount'],
        #         finally_budjet=request.POST['Amount'],
        #         end_of_date=request.POST['enddate'],
        #         priority=request.POST['Prioritys'],
        #         mail_id=request.POST['email'],
        #         status=request.POST['satus'],
        #         additional_remarks=request.POST['comments'],
        #         call_back_comments=request.POST['Remarks'],
        #         call_back=request.POST['callbackdate'],
        #         created_by = request.user,
        #         created_date = datetime.datetime.now(),
        #         updated_by = request.user,
        #         updated_date = datetime.datetime.now(),
        #     )

            # selected_products = ProductTable.objects.filter(Product_Name__in=selected_product_names)
            # new_lead.products.set(selected_products)

            # new_lead.save()
    
            # UserActivity.objects.create(
            #     user=request.user,
            #     timestamp=timezone.now(),
            #     lable = f"{new_lead.org_name}",
            #     action="created lead",
            #     content_type=ContentType.objects.get_for_model(Lead),
            #     object_id=new_lead.pk,
            # )
            # return redirect('leads')
        
        # messages.error(request, f"{e}")
        return redirect('leads')

    context = {
        "leads": "activete",
        'All_Leads': Lead.objects.all(),
        "Teams": Team.objects.all(),
        "Org_Type": OrgType.objects.all(),
        "Locations": Location.objects.all(),
        "citys": City.objects.all(),
        "lead_names": LeadTable.objects.all(),
        "BUSINESS_TYPE_CHOICES": Lead.BUSINESS_TYPE_CHOICES,
        "Products": ProductTable.objects.all(),
        "Prioritys": Lead.PRIORITY_CHOICES,
        "Statuss": Lead.STATUS_CHOICES,
        'Org_Name': OrgName.objects.all(),
        "users": CustomUser.objects.filter(is_admin=True, is_active=True),
    }

    return render(request, 'Revaa/crm_leads_page.html', context)


@login_required(login_url='/login')
def without_view(request):
    context = {
        "leads": "activete",
        'All_Leads': Lead.objects.filter(is_customer=False),
        "Teams": Team.objects.all(),
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