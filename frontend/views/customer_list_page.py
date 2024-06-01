from django.shortcuts import render, redirect
from frontend.models import CustomUser, Lead, OrgType, Location, City, LeadTable, ProductTable, customertable, OrgName, UserActivity
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
import datetime

@login_required(login_url='/login')
def customer_page_view(request):
    if request.method == 'POST':
        client_photo = request.FILES.get('company_logo', '')
        client_name = request.POST.get('Client_name', '')
        client_number = request.POST.get('Client_number', '')
        company_name = request.POST.get('Company_name', '')
        company_type_id = request.POST.get('Company_type', '')
        country_name = request.POST.get('Country', '')
        city_name = request.POST.get('city', '')
        referral_name = request.POST.get('lead_name', '')
        business_type = request.POST.get('bussinesstype', '')
        proposal_amount = request.POST.get('Amount', '')
        end_of_date = request.POST.get('enddate', '')
        priority = request.POST.get('Prioritys', '')
        mail_id = request.POST.get('email', None)
        status = request.POST.get('satus', '')
        additional_remarks = request.POST.get('comments', '')
        call_back_comments = request.POST.get('Remarks', '')
        call_back = request.POST.get('callbackdate', '')
        selected_product_names = request.POST.getlist('products')

        # Validate required fields and add error messages
        if not client_name:
            messages.error(request, "Client name is required.")
        if not client_number:
            messages.error(request, "Client number is required.")
        if not company_name:
            messages.error(request, "Company name is required.")
        if not company_type_id:
            messages.error(request, "Company type is required.")
        if not country_name:
            messages.error(request, "Country is required.")
        if not city_name:
            messages.error(request, "City is required.")
        if not referral_name:
            messages.error(request, "Referral name is required.")
        if not business_type:
            messages.error(request, "Business type is required.")
        if not proposal_amount:
            messages.error(request, "Proposal amount is required.")
        if not end_of_date:
            messages.error(request, "End date is required.")
        if not priority:
            messages.error(request, "Priority is required.")
        if not status:
            messages.error(request, "Status is required.")
        if not additional_remarks:
            messages.error(request, "Additional remarks are required.")
        if not call_back_comments:
            messages.error(request, "Call back comments are required.")
        if not call_back:
            messages.error(request, "Call back date is required.")
        if not selected_product_names:
            messages.error(request, "Please select products.")

        try:
            company_type = OrgType.objects.get(pk=company_type_id)
            country = Location.objects.get(location=country_name)
            city = City.objects.get(city=city_name)
            referral = LeadTable.objects.get(Lead_Name=referral_name)

            new_lead = customertable.objects.create(
                client_name=client_name,
                client_number=client_number,
                org_name=company_name,
                org_type=company_type,
                location=country,
                city=city,
                lead_name=referral,
                business_type=business_type,
                amount=proposal_amount,
                end_of_date=end_of_date,
                priority=priority,
                mail_id=mail_id,
                status=status,
                comment=additional_remarks,
                remarks=call_back_comments,
                follow_up=call_back,
                created_by=request.user,
                created_date=datetime.datetime.now(),
                updated_by=request.user,
                updated_date=datetime.datetime.now(),
            )

            if client_photo:
                new_lead.org_img = client_photo

            selected_products = ProductTable.objects.filter(Product_Name__in=selected_product_names)
            new_lead.products.set(selected_products)

            new_lead.save()

            UserActivity.objects.create(
                user=request.user,
                timestamp=timezone.now(),
                lable = f"Create customer, {new_lead.client_name}, {new_lead.org_name} company for customer list",
                action="Created",
                content_type=ContentType.objects.get_for_model(Lead),
                object_id=new_lead.pk,
            )
            return redirect('coustomer')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('coustomer')

    context = {
        "customer": "activete",
        'All_Customers': customertable.objects.all(),
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

    return render(request, 'Revaa/customer_template.html', context)
