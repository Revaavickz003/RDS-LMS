from django.contrib import messages
from django.shortcuts import redirect
from frontend.models import Lead, OrgName, OrgType, Location, City, LeadTable, ProductTable
import pandas as pd
from datetime import datetime
from django.http import HttpResponse
from openpyxl import Workbook

def LeadImportView(request):
    if request.method == 'POST':
        import_file = request.FILES.get('import_file')
        if import_file and import_file.name.endswith('.xlsx'):
            try:
                df = pd.read_excel(import_file)

                for index, row in df.iterrows():
                    org_name = row.get('Company Name')
                    
                    # Handle Business Type
                    business_type = row.get('Business type')
                    if not business_type:
                        messages.error(request, f"Error on row {index + 2}: Business Type is missing.")
                        continue
                    elif business_type not in dict(Lead.BUSINESS_TYPE_CHOICES).keys():
                        messages.error(request, f"Error on row {index + 2}: Invalid Business Type '{business_type}'.")
                        continue
                        
                    try:
                        org_type = OrgType.objects.get_or_create(org_type=row.get('Company Type'))[0]
                        location = Location.objects.get_or_create(location=row.get('Location'))[0]
                        city = City.objects.get_or_create(city=row.get('City'))[0]
                        lead_name = LeadTable.objects.get_or_create(Lead_Name=row.get('Lead'))[0]

                        # Handle products
                        product_names = [p.strip() for p in str(row.get('Products')).split(',')]
                        if not product_names:
                            messages.warning(request, f"No products specified for company '{org_name}'.")
                            continue
                        try:
                            selected_products = []
                            for product_name in product_names:
                                product = ProductTable.objects.get(Product_Name=product_name)
                                selected_products.append(product)
                        except:
                            messages.warning(request, f"Invalid products for company '{org_name}'.")
                            continue

                        # Handle end_of_date
                        end_of_date = row.get('End of Date', '')
                        if not end_of_date:
                            end_of_date = datetime.now().date()
                        

                        # Handle follow_up
                        follow_up_date_str = row.get('Follow up', '')
                        if not follow_up_date_str:
                            follow_up_date_str = datetime.now().date()

                        # Handle Company Name
                        if not org_name:
                            messages.error(request, f"Error on row {index + 2}: Company Name is missing.")
                            continue

                        existing_org = OrgName.objects.filter(Org_Name=org_name).first()
                        if existing_org:
                            messages.error(request, f"Error on row {index + 2}: Company '{org_name}' already exists.")
                            continue

                        try:
                            new_company = OrgName.objects.create(Org_Name=org_name)
                        except Exception as e:
                            messages.error(request, f"Error creating company '{org_name}': {str(e)}")
                            continue

                        new_lead = Lead.objects.create(
                            client_name=row.get('Client Name', ''),
                            client_number=row.get('Client Number', ''),
                            org_type=org_type,
                            location=location,
                            city=city,
                            lead_name=lead_name,
                            business_type=business_type,
                            amount=int(row.get('Amount', '')),
                            end_of_date=end_of_date,
                            priority=row.get('Priority', ''),
                            mail_id=row.get('Email', ''),
                            status=row.get('Status', ''),
                            comment=row.get('Comments', ''),
                            remarks=row.get('Remark', ''),
                            follow_up=follow_up_date_str,
                            created_by=request.user,
                            updated_by=request.user,
                            org_name=new_company,
                        )
                        new_lead.products.set(selected_products)
                        print("Yes success")

                    except Exception as e:
                        messages.error(request, f"Error creating lead on row {index + 2}: {str(e)}")
                        continue
                return redirect('leads')
            except Exception as e:
                messages.error(request, f"Error reading Excel file: {str(e)}")
                return redirect('leads')
    return redirect('leads')


# Export data

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
        'Location', 
        'City', 
        'Business Type',
        'Products',
        'Amount',
        'Is Customer',
        'Created Date',
        'End of Date',
        'Lead Name', 
        'Priority',
        'Mail ID', 
        'Status', 
        'Comment', 
        'Remarks', 
        'Follow Up', 
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
            lead.org_name, 
            lead.org_type.org_type,
            lead.location.location, 
            lead.city.city, 
            lead.business_type,
            product_names,  # Modify this line to include product names as a comma-separated string
            lead.amount,
            lead.is_customer,
            lead.created_date,
            lead.end_of_date,
            lead.lead_name.Lead_Name,
            lead.priority, 
            lead.mail_id, 
            lead.status,
            lead.comment, 
            lead.remarks, 
            lead.follow_up, 
            lead.created_by.username, 
            lead.updated_by.username, 
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