from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from frontend.models import *

@login_required(login_url='/login')
def maindashbord_page_view(request):

    # Retrieve lead products
    lead_products = ProductTable.objects.filter(lead__isnull=False).distinct()
    lead_product_counts = [lead_product.lead_set.count() for lead_product in lead_products]

    # Retrieve customer products
    customer_products = ProductTable.objects.filter(customertable__isnull=False).distinct()
    customer_product_counts = [customer_product.customertable_set.count() for customer_product in customer_products]

    # Combine product names from both sources
    lead_product_names = list(lead_products.values_list('Product_Name', flat=True))
    customer_product_names = list(customer_products.values_list('Product_Name', flat=True))

    # Combine product counts from both sources
    lead_product_counts = lead_product_counts
    customer_product_counts = customer_product_counts

    context = {
        'leaddashbord':'activete',
        'lead_products': lead_product_names,
        'lead_product_counts': lead_product_counts,
        'customer_products': customer_product_names,
        'customer_product_counts': customer_product_counts,
        'over_all_leads': Lead.objects.all().count(),
        'over_all_customer': customertable.objects.all().count(),
        'convert_to_customer': Lead.objects.filter(is_customer=True).count(),
        'with_out_customer': Lead.objects.filter(is_customer=False).count(),
        'Recent_actions': UserActivity.objects.filter(user=request.user).select_related('user')[::-1][:5]
    }
    return render(request, 'Revaa/crm_index.html', context)
