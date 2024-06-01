import os
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from frontend.models import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

@login_required(login_url='/login/')
def convert_customer(request, id):
    try:
        get_data = Lead.objects.get(id=id)
        get_data.is_customer = True
        get_data.save()
    except Lead.DoesNotExist:
        messages.error(request, "Lead does not exist")
        return redirect(reverse('leads'))
    
    # Check if a customer with the same organization name already exists
    existing_customer = customertable.objects.filter(org_name=get_data.company_name).first()
    if existing_customer:
        messages.success(request, "The lead already exists for Customer")
        return redirect(reverse('leads'))
    
    try:
        # Retrieve ForeignKey objects directly from the Lead instance, if they exist
        orgtype = OrgType.objects.filter(org_type=get_data.company_type).first()
        location = Location.objects.filter(location=get_data.country).first()
        city = City.objects.filter(city=get_data.city).first()
        leadname = LeadTable.objects.filter(Lead_Name=get_data.reffral_name).first()

        if not orgtype or not location or not city or not leadname:
            messages.error(request, "One or more related objects do not exist")
            return redirect(reverse('leads'))

        # Create the customertable instance
        new_customer = customertable.objects.create(
            org_img=get_data.company_img.name,
            client_name=get_data.client_name,
            client_number=get_data.client_number,
            org_name=get_data.company_name,
            org_type=orgtype,
            location=location,
            city=city,
            lead_name=leadname,
            business_type=get_data.business_type,
            amount=get_data.finally_budjet,
            end_of_date=get_data.end_of_date,
            priority=get_data.priority,
            mail_id=get_data.mail_id,
            status=get_data.status,
            comment=get_data.additional_remarks,
            remarks=get_data.call_back_comments,
            follow_up=get_data.call_back,
            created_by=request.user,
            updated_by=request.user,
        )

        # Add products to the new customer
        new_customer.products.set(get_data.products.all())

        # Save the new customer instance after adding products
        new_customer.save()

        # Create a new lead history entry
        UserActivity.objects.create(
            user=request.user,
            timestamp=timezone.now(),
            lable=f"{new_customer.org_name}",
            action="Convert lead to customer",
            content_type=ContentType.objects.get_for_model(customertable),
            object_id=new_customer.pk,
        )

        return redirect(reverse('editlead', kwargs={'pk': get_data.pk}))
    except Exception as e:
        messages.error(request, f"Error occurred while converting lead to customer: {e}")
        return redirect(reverse('leads'))
