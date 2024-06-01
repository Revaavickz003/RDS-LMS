from django.shortcuts import render, redirect
from django.urls import reverse
from frontend.models import customertable, OrgType, Location, City, LeadTable, ProductTable, UserActivity, CustomUser
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
import datetime as dt


@login_required(login_url='/login')
def view_sing_customer(request, pk):
    try:
        get_data = customertable.objects.get(id=pk)
    except customertable.DoesNotExist:
        messages.error(request, 'Invalid customer, select the customer from the customer table')
        return redirect('coustomer')

    formatted_end_of_date = get_data.end_of_date.strftime('%d-%m-%Y')
    formatted_follow_up = get_data.follow_up.strftime('%d-%m-%Y')

    if request.method == 'POST':
        org_img = request.FILES.get('company_logo', '')
        client_name = request.POST.get('client_name', '')
        client_number = request.POST.get('client_number', '')
        company_type_id = request.POST.get('Company_type', '')
        country_name = request.POST.get('Country', '')
        city_name = request.POST.get('city', '')
        referral_name = request.POST.get('lead_name', '')
        business_type = request.POST.get('bussinesstype', '')
        amount = request.POST.get('amount', '')
        priority = request.POST.get('Prioritys', '')
        mail_id = request.POST.get('email', '')
        status = request.POST.get('satus', '')
        additional_remarks = request.POST.get('comments', '')
        call_back_comments = request.POST.get('remarks', '')
        selected_product_names = request.POST.getlist('products')
        end_of_date = request.POST.get('enddate', '')
        call_back = request.POST.get('callbackdate', '')

        # Validate required fields
        errors = False

        if not client_name:
            messages.error(request, "Client name is required.")
            errors = True
        if not client_number:
            messages.error(request, "Client number is required.")
            errors = True
        if not company_type_id:
            messages.error(request, "Company type is required.")
            errors = True
        if not country_name:
            messages.error(request, "Country is required.")
            errors = True
        if not city_name:
            messages.error(request, "City is required.")
            errors = True
        if not referral_name:
            messages.error(request, "Referral name is required.")
            errors = True
        if not business_type:
            messages.error(request, "Business type is required.")
            errors = True
        if not amount:
            messages.error(request, "Amount is required.")
            errors = True
        if not priority:
            messages.error(request, "Priority is required.")
            errors = True
        if not status:
            messages.error(request, "Status is required.")
            errors = True
        if not additional_remarks:
            messages.error(request, "Additional remarks are required.")
            errors = True
        if not call_back_comments:
            messages.error(request, "Call back comments are required.")
            errors = True
        if not end_of_date:
            messages.error(request, "End date is required.")
            errors = True
        if not call_back:
            messages.error(request, "Call back date is required.")
            errors = True
        if not selected_product_names:
            messages.error(request, "Please select products.")
            errors = True

        if errors:
            return redirect(reverse('editcustomer', kwargs={'pk': int(get_data.pk)}))

        try:
            company_type = OrgType.objects.get(pk=company_type_id)
            country = Location.objects.get(location=country_name)
            city = City.objects.get(city=city_name)
            referral = LeadTable.objects.get(Lead_Name=referral_name)

            enddate = datetime.strptime(end_of_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            callbackdate = datetime.strptime(call_back, "%d-%m-%Y").strftime("%Y-%m-%d")

            if org_img:
                get_data.org_img = org_img

            get_data.client_name = client_name
            get_data.client_number = client_number
            get_data.org_type = company_type
            get_data.location = country
            get_data.city = city
            get_data.lead_name = referral
            get_data.business_type = business_type
            get_data.amount = amount
            get_data.end_of_date = enddate
            get_data.priority = priority
            get_data.mail_id = mail_id
            get_data.status = status
            get_data.comment = additional_remarks
            get_data.remarks = call_back_comments
            get_data.follow_up = callbackdate

            selected_products = ProductTable.objects.filter(Product_Name__in=selected_product_names)
            get_data.products.set(selected_products)

            get_data.save()

            # Create a new lead history entry
            UserActivity.objects.create(
                user=request.user,
                timestamp=dt.datetime.now(),
                lable = f"Update customer, {get_data.client_name}, {get_data.org_name} company",
                action="Updated",
                content_type=ContentType.objects.get_for_model(customertable),
                object_id=get_data.pk,
            )

            messages.success(request, "Customer updated successfully.")
            return redirect(reverse('editcustomer', kwargs={'pk': int(get_data.pk)}))

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect(reverse('editcustomer', kwargs={'pk': int(get_data.pk)}))

    context = {
        "customer": "activete",
        "get_data": get_data,
        "Org_Type": OrgType.objects.all(),
        "Locations": Location.objects.all(),
        "citys": City.objects.all(),
        "lead_names": LeadTable.objects.all(),
        "BUSINESS_TYPE_CHOICES": customertable.BUSINESS_TYPE_CHOICES,
        "Products": ProductTable.objects.all(),
        "Prioritys": customertable.PRIORITY_CHOICES,
        "Statuss": customertable.STATUS_CHOICES,
        "formatted_end_of_date": formatted_end_of_date,
        "formatted_follow_up": formatted_follow_up,
    }
    return render(request, 'Revaa/single_customer_page.html', context)
