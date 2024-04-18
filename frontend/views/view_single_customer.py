from django.shortcuts import render, redirect
from django.urls import reverse
from frontend.models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages

# Create your views here.

@login_required(login_url='/login')
def view_sing_customer(request, pk):
    try:
        get_data = customertable.objects.get(id=pk)
    except:
        messages.error(request, 'Invalid customer, select the customer, only customer table')
        return redirect('coustomer')
    
    formatted_end_of_date = get_data.end_of_date.strftime('%d-%m-%Y')
    formatted_follow_up = get_data.follow_up.strftime('%d-%m-%Y')

    if request.method == 'POST':
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
            get_data.org_img = org_img
        get_data.client_name = request.POST.get('client_name')
        get_data.client_number = request.POST.get('client_number')
        get_data.org_type = Create_Company_type
        get_data.location = Locations
        get_data.city = city_name
        get_data.lead_name = lead_name
        get_data.business_type = request.POST.get('bussinesstype')
        get_data.amount = request.POST.get('amount')
        get_data.end_of_date = enddate
        get_data.priority = request.POST.get('Prioritys')
        get_data.mail_id = request.POST.get('email')
        get_data.status = request.POST.get('satus')
        get_data.comment = request.POST.get('comments')
        get_data.remarks = request.POST.get('remarks')
        get_data.follow_up = callbackdate

        selected_products = ProductTable.objects.filter(Product_Name__in=selected_product_names)
        get_data.products.set(selected_products)

        get_data.save()

        return redirect(reverse('editcustomer', kwargs={'pk': int(get_data.pk)}))


    context = {
        "customer": "activete",
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
    return render(request, 'Revaa/single_customer_page.html', context)
