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

        try:
            selected_product_names = request.POST.getlist('products')
        except:
            return render(request, 'Revaa/crm_template.html', {'error': 'Invalid lead'})
        
        # Formated dates
        # End Date
        enddate = request.POST.get('enddate')
        enddate = datetime.strptime(enddate, "%d-%m-%Y")
        enddate = enddate.strftime("%Y-%m-%d")

        # Follow up date
        callbackdate = request.POST.get('callbackdate')
        callbackdate = datetime.strptime(callbackdate, "%d-%m-%Y")
        callbackdate = callbackdate.strftime("%Y-%m-%d")

        org_img = request.FILES.get('company_logo')
        if org_img:
            get_data.company_img = org_img
        get_data.client_name = request.POST.get('client_name')
        get_data.client_number = request.POST.get('client_number')
        get_data.company_type = Create_Company_type
        get_data.country = Locations
        get_data.city = city_name
        get_data.reffral_name = lead_name
        get_data.business_type = request.POST.get('bussinesstype')
        get_data.proposal_amount = request.POST.get('amount')
        get_data.end_of_date = enddate
        get_data.priority = request.POST.get('Prioritys')
        get_data.mail_id = request.POST.get('email')
        get_data.status = request.POST.get('satus')
        get_data.call_back_comments = request.POST.get('comments')
        get_data.additional_remarks = request.POST.get('remarks')
        get_data.call_back = callbackdate

        selected_products = ProductTable.objects.filter(Product_Name__in=selected_product_names)
        get_data.products.set(selected_products)

        get_data.save()
        
        # Create a new lead history entry
        UserActivity.objects.create(
        user=request.user,
        timestamp=timezone.now(),
        lable = f"{get_data.org_name}",
        action="Updated lead",
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
