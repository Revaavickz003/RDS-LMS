from django.contrib import messages
from django.shortcuts import redirect
from frontend.models import Lead, OrgType, Location, City, LeadTable, ProductTable, UserActivity, OrgName
import pandas as pd
from datetime import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

def LeadImportView(request):
    if request.method == 'POST':
        import_file = request.FILES.get('import_file')
        if import_file and import_file.name.endswith('.xlsx'):
            try:
                df = pd.read_excel(import_file)

                for index, row in df.iterrows():
                    company_name = row.get('Company Name')

                    # Handle Business Type
                    business_type = row.get('Business type')
                    if not business_type:
                        messages.error(request, f"Error on row {index + 2}: Business Type is missing.")
                        continue
                    elif business_type not in dict(Lead.BUSINESS_TYPE_CHOICES).keys():
                        messages.error(request, f"Error on row {index + 2}: Invalid Business Type '{business_type}'.")
                        continue

                    try:
                        # Fetch existing entries
                        org_type = OrgType.objects.filter(org_type=row.get('Company Type')).first()
                        country = Location.objects.filter(location=row.get('Location')).first()
                        city = City.objects.filter(city=row.get('City')).first()
                        reffral_name = LeadTable.objects.filter(Lead_Name=row.get('Referral Name')).first()

                        # If any required foreign key is missing, log an error and skip the row
                        if not org_type:
                            messages.error(request, f"Error on row {index + 2}: Company Type '{row.get('Company Type')}' does not exist.")
                            continue
                        if not country:
                            messages.error(request, f"Error on row {index + 2}: Location '{row.get('Location')}' does not exist.")
                            continue
                        if not city:
                            messages.error(request, f"Error on row {index + 2}: City '{row.get('City')}' does not exist.")
                            continue
                        if not reffral_name:
                            messages.error(request, f"Error on row {index + 2}: Referral Name '{row.get('Referral Name')}' does not exist.")
                            continue

                        # Handle products
                        product_names = [p.strip() for p in str(row.get('Products')).split(',')]
                        if not product_names:
                            messages.warning(request, f"No products specified for company '{company_name}'.")
                            continue
                        try:
                            selected_products = []
                            for product_name in product_names:
                                product = ProductTable.objects.filter(Product_Name=product_name).first()
                                if not product:
                                    raise ValueError(f"Product '{product_name}' does not exist.")
                                selected_products.append(product)
                        except ValueError as e:
                            messages.warning(request, f"Invalid products for company '{company_name}': {e}")
                            continue

                        # Handle end_of_date
                        end_of_date = row.get('End of Date', '')
                        if not end_of_date:
                            end_of_date = datetime.now().date()
                        else:
                            end_of_date = datetime.strptime(end_of_date, '%Y-%m-%d').date()

                        # Handle call_back
                        call_back_date_str = row.get('Call Back', '')
                        if not call_back_date_str:
                            call_back_date_str = datetime.now().date()
                        else:
                            call_back_date_str = datetime.strptime(call_back_date_str, '%Y-%m-%d').date()

                        # Handle Company Name
                        if not company_name:
                            messages.error(request, f"Error on row {index + 2}: Company Name is missing.")
                            continue

                        # Check for duplicate leads with the same company_name and products
                        existing_leads = Lead.objects.filter(
                            company_name=company_name,
                            products__in=selected_products
                        ).distinct()

                        if existing_leads.exists():
                            messages.error(request, f"Error on row {index + 2}: Lead for company '{company_name}' with the same products already exists.")
                            continue

                        new_lead = Lead.objects.create(
                            client_name=row.get('Client Name', ''),
                            client_number=row.get('Client Number', ''),
                            company_name=company_name,
                            company_type=org_type,
                            country=country,
                            city=city,
                            reffral_name=reffral_name,
                            business_type=business_type,
                            proposal_amount=row.get('Proposal Amount', 0),
                            finally_budjet=row.get('Finally Budget', 0),
                            end_of_date=end_of_date,
                            priority=row.get('Priority', ''),
                            mail_id=row.get('Email', ''),
                            status=row.get('Status', ''),
                            additional_remarks=row.get('Additional Remarks', ''),
                            call_back_comments=row.get('Call Back Comments', ''),
                            call_back=call_back_date_str,
                            created_by=request.user,
                            updated_by=request.user,
                            created_date=datetime.now().date(),
                            updated_date=datetime.now().date(),
                        )
                        new_lead.products.set(selected_products)

                        UserActivity.objects.create(
                            user=request.user,
                            timestamp=timezone.now(),
                            lable = f"Created {new_lead.company_name} for leads list",
                            action="Created",
                            content_type=ContentType.objects.get_for_model(Lead),
                            object_id=new_lead.pk,
                        )

                    except Exception as e:
                        messages.error(request, f"Error creating lead on row {index + 2}: {str(e)}")
                        continue
                return redirect('leads')
            except Exception as e:
                messages.error(request, f"Error reading Excel file: {str(e)}")
                return redirect('leads')
    return redirect('leads')



# Export data

from django.http import HttpResponse
from openpyxl import Workbook
from frontend.models import Lead

def export_leads_to_excel(request):
    # Query all leads
    leads = Lead.objects.all()

    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Define column headers
    headers = [
        'Client Name', 
        'Client Number', 
        'Company Name', 
        'Company Type',
        'Country', 
        'City', 
        'Business Type',
        'Products',
        'Proposal Amount',
        'Finally Budget',
        'End of Date',
        'Priority',
        'Mail ID', 
        'Status', 
        'Additional Remarks', 
        'Call Back Comments', 
        'Call Back', 
        'Is Customer',
        'Created Date',
        'Created By', 
        'Updated By', 
        'Updated Date'
    ]
    ws.append(headers)
    # Append lead data to worksheet
    for lead in leads:
        product_names = ", ".join([product.Product_Name for product in lead.products.all()])
        lead_data = [
            lead.client_name, 
            lead.client_number, 
            lead.company_name, 
            lead.company_type.org_type,
            lead.country.location, 
            lead.city.city, 
            lead.business_type,
            product_names,  # Modify this line to include product names as a comma-separated string
            lead.proposal_amount,
            lead.finally_budjet,
            lead.end_of_date,
            lead.priority, 
            lead.mail_id, 
            lead.status,
            lead.additional_remarks, 
            lead.call_back_comments, 
            lead.call_back, 
            lead.is_customer,
            lead.created_date,
            lead.created_by.username if lead.created_by else '', 
            lead.updated_by.username if lead.updated_by else '', 
            lead.updated_date
        ]
        ws.append(lead_data)

    # Save the workbook to a file
    filename = 'leads_export.xlsx'
    wb.save(filename)

    # Serve the XLSX file as a download response
    with open(filename, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        return response