from django.utils import timezone
from django.shortcuts import render, redirect
from frontend.models import Lead, OrgType, Location, City, LeadTable, ProductTable, Team, OrgName, CustomUser, UserActivity
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

@login_required(login_url='/login')
def crm_page_view(request):
    if request.method == 'POST':
        try:
            org_name = request.POST['Company_name']
            existing_org = OrgName.objects.get(Org_Name=org_name)
            messages.error(request, "This company already exists.")
            return redirect('leads')
        except:
            new_company = OrgName.objects.create(Org_Name=org_name)
            new_company.save()

        try:
            Create_Company_type = OrgType.objects.get(org_type=request.POST['Company_type'])
        except:
            Create_Company_type = OrgType.objects.create(org_type=request.POST['Company_type'])

        try:
            Locations = Location.objects.get(location=request.POST['location'])
        except:
            Locations = Location.objects.create(location=request.POST['location'])

        try:
            city_name = City.objects.get(city=request.POST['city'])
        except:
            city_name = City.objects.create(city=request.POST['city'])

        try:
            lead_name = LeadTable.objects.get(Lead_Name=request.POST['lead_name'])
        except:
            lead_name = LeadTable.objects.create(Lead_Name=request.POST['lead_name'])

        try:
            selected_product_names = request.POST.getlist('products')
        except:
            return render(request, 'Revaa/crm_template.html', {'error': 'Invalid lead'})


        new_lead = Lead.objects.create(
            client_name=request.POST['Client_name'],
            client_number=request.POST['Client_number'],
            org_name=request.POST['Company_name'],
            org_type=Create_Company_type,
            location=Locations,
            city=city_name,
            lead_name=lead_name,
            business_type=request.POST['bussinesstype'],
            amount=request.POST['Amount'],
            end_of_date=request.POST['enddate'],
            priority=request.POST['Prioritys'],
            mail_id=request.POST['email'],
            status=request.POST['satus'],
            comment=request.POST['comments'],
            remarks=request.POST['Remarks'],
            follow_up=request.POST['callbackdate'],
            created_by = request.user,
            updated_by = request.user,
        )

        selected_products = ProductTable.objects.filter(Product_Name__in=selected_product_names)
        new_lead.products.set(selected_products)

        new_lead.save()
        UserActivity.objects.create(
            user=request.user,
            timestamp=timezone.now(),
            lable = f"{new_lead.org_name}",
            action="created lead",
            content_type=ContentType.objects.get_for_model(Lead),
            object_id=new_lead.pk,
        )
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
        "users": CustomUser.objects.exclude(is_admin=True, is_active=True),
    }

    return render(request, 'Revaa/crm_leads_page.html', context)
