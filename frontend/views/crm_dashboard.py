from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from frontend.models import *
from datetime import datetime, timedelta, date
from collections import Counter

@login_required(login_url='/login')
def maindashbord_page_view(request):
    current_date = datetime.now()
    # Determine the start and end of the financial year
    if current_date.month >= 4:  # April or later
        fiscal_year_start = date(current_date.year, 4, 1)
        fiscal_year_end = date(current_date.year + 1, 3, 31)
    else:  # Before April
        fiscal_year_start = date(current_date.year - 1, 4, 1)
        fiscal_year_end = date(current_date.year, 3, 31)
    
    # Filter leads within the financial year
    fiscal_year_leads = Lead.objects.filter(
        created_date__gte=fiscal_year_start,
        created_date__lte=fiscal_year_end
    )
    
    # Count the statuses of the filtered leads
    lead_status_counts = Counter(fiscal_year_leads.values_list('status', flat=True))
    lead_statuses = list(lead_status_counts.keys())
    lead_status_values = list(lead_status_counts.values())
    

    # This month Leads count
    this_month_leads =fiscal_year_leads.filter(created_date__month=datetime.now().month, created_date__year=datetime.now().year)
    this_month_leads_count = this_month_leads.count()
    prev_month_leads = fiscal_year_leads.filter(created_date__month=datetime.now().month-1)
    prev_month_leads_count = prev_month_leads.count()
    diff = this_month_leads_count - prev_month_leads_count

    # Last 30 days Leads
    last_30_days_leads = fiscal_year_leads.filter(created_date__gte=datetime.now() - timedelta(days=30))
    last_30_days_leads_count = last_30_days_leads.count()


    # Prospective Leads
    prospective_leads = fiscal_year_leads.filter(status__in=['Fresh', 'Follow up', 'Proposed', 'Hold', 'Closed'])
    prospective_leads_count = prospective_leads.count()

    # Future prospective
    Monthly_prospective = this_month_leads.filter(status__in=['Fresh', 'Follow up', 'Proposed', 'Hold', 'Closed'])
    Monthly_prospective_count = Monthly_prospective.count()

    # Commercial leads
    last_30_days_prospective = last_30_days_leads.filter(status__in=['Fresh', 'Follow up', 'Proposed', 'Hold', 'Closed'])
    last_30_days_prospective_count = last_30_days_prospective.count()

    # Span Leads
    span_leads_count = Lead.objects.filter(status__in=['Closed', 'Not Interested' 'Do Not Disturb'])
    span_leads_count = span_leads_count.count()

                                                               

    context = {
        'leaddashbord':'activete',
        'this_month': datetime.now().strftime("%b").upper(),
        'this_month_leads_count':this_month_leads_count,
        'prev_month_leads_count_diff':diff,
        'last_30_days_leads_count':last_30_days_leads_count,
        'prospective_leads_count':prospective_leads_count,
        'Monthly_prospective_count':Monthly_prospective_count,
        'last_30_days_prospective_count':last_30_days_prospective_count,
        'span_leads_count':span_leads_count,

        'lead_statuses': lead_statuses,
        'lead_status_values': lead_status_values,
        'over_all_leads': fiscal_year_leads.count(),
        'over_all_customer': customertable.objects.all().count(),
        'convert_to_customer': Lead.objects.filter(is_customer=True).count(),
        'with_out_customer': Lead.objects.filter(is_customer=False).count(),
        'Recent_actions': UserActivity.objects.filter(user=request.user).select_related('user')[::-1][:5]
    }
    return render(request, 'Revaa/crm_index.html', context)
