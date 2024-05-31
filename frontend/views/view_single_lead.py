from django.shortcuts import render, redirect
from django.urls import reverse
from frontend.models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

@login_required(login_url='/login')
def view_sing_lead(request, pk):
    try:
        get_data = Lead.objects.get(id=pk)
    except:
        messages.error(request, 'Invalid lead, select the leads only leads table')
        return redirect('leads')
    formatted_end_of_date = get_data.end_of_date.strftime('%d-%m-%Y')
    formatted_follow_up = get_data.call_back.strftime('%d-%m-%Y')

    if request.method == 'POST':
        client_name = request.POST.get('client_name', '')
        client_number = request.POST.get('client_number', '')
        company_type = request.POST.get('Company_type', '')
        country = request.POST.get('Country', '')
        city = request.POST.get('city', '')
        reffral_name = request.POST.get('lead_name', '')
        business_type = request.POST.get('bussinesstype', '')
        proposal_amount = request.POST.get('proposal_amount', '')
        finally_budjet = request.POST.get('finally_budjet', '')
        priority = request.POST.get('Prioritys', '')
        mail_id = request.POST.get('email', '')
        status = request.POST.get('satus', '')
        additional_remarks = request.POST.get('comments', '')
        call_back_comments = request.POST.get('remarks', '')

        try:
            company_type = OrgType.objects.get(pk = company_type)
        except:
            messages.error(request, "Please select Company type")
        try:
            country = Location.objects.get(location = country)
        except:
            messages.error(request, "Please select Country")
        try:
            city = City.objects.get(city = city)
        except:
            messages.error(request, "Please select City")
        try:
            Lead_name = LeadTable.objects.get(Lead_Name = reffral_name)
        except:
            messages.error(request, "Please select Reffral name")

        try:
            selected_product_names = request.POST.getlist('products')
        except:
            return render(request, 'Revaa/crm_template.html', {'error': 'Invalid lead'})
        # End Date
        end_of_date = request.POST.get('enddate', '')
        enddate = datetime.strptime(end_of_date, "%d-%m-%Y")
        enddate = enddate.strftime("%Y-%m-%d")
        # Follow up date
        call_back = request.POST.get('callbackdate', '')
        callbackdate = datetime.strptime(call_back, "%d-%m-%Y")
        callbackdate = callbackdate.strftime("%Y-%m-%d")
        org_img = request.FILES.get('company_logo', '')
        print(org_img)

        if org_img:
            get_data.company_img = org_img
            print("Save")
        get_data.client_name = client_name
        get_data.client_number = client_number
        get_data.company_type = company_type
        get_data.country = country
        get_data.city = city
        get_data.reffral_name = Lead_name
        get_data.business_type = business_type
        get_data.proposal_amount = proposal_amount
        get_data.finally_budjet = finally_budjet
        get_data.end_of_date = enddate
        get_data.priority = priority
        get_data.mail_id = mail_id
        get_data.status = status
        get_data.call_back_comments = additional_remarks
        get_data.additional_remarks = call_back_comments
        get_data.call_back = callbackdate

        selected_products = ProductTable.objects.filter(Product_Name__in=selected_product_names)
        get_data.products.set(selected_products)

        get_data.save()
        
        # Create a new lead history entry
        UserActivity.objects.create(
        user=request.user,
        timestamp=timezone.now(),
        lable = f"Update Lead, {get_data.client_name}, {get_data.company_name} company",
        action="Updated",
        content_type=ContentType.objects.get_for_model(Lead),
        object_id=get_data.pk,
    )

        return redirect(reverse('editlead', kwargs={'pk': get_data.pk}))

    context = {
        "leads": "activete",
        "get_data": get_data,
        "Org_Type": OrgType.objects.all(),
        "Locations": Location.objects.all(),
        "citys": City.objects.all(),
        "lead_names": LeadTable.objects.all(),
        "BUSINESS_TYPE_CHOICES": Lead.BUSINESS_TYPE_CHOICES,
        "Products": ProductTable.objects.all(),
        "Prioritys": Lead.PRIORITY_CHOICES,
        "Statuss": Lead.STATUS_CHOICES,
        "formatted_end_of_date": formatted_end_of_date,
        "formatted_follow_up": formatted_follow_up,
    }
    return render(request, 'Revaa/single_lead_page.html', context)
