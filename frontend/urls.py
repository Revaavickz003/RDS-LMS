from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from frontend.views import (
    convert_customer,
    crm_dashboard,
    lead_import_data_export_data,
    leads_list_page,
    settings_view,
    login_page_view,
    view_single_lead,
    customer_list_page,
    leads_filter_view,
    view_single_customer,
    customer_import_data_and_export_data,
    customer_filter,
    basic_functions,
    leads_filter,
    )

urlpatterns = [

    # sidebar Views
    path('', crm_dashboard.maindashbord_page_view, name="crmdashboard"),
    path('setting/', settings_view.setting, name='setting'),
    
    #  Leads
    path('crm/leads/', leads_list_page.crm_page_view, name="leads"),
    path('crm/without_view/', leads_list_page.without_view, name="without_view"),
    path('crm/leads/<int:pk>/edit/',view_single_lead.view_sing_lead, name='editlead'),
    path('crm/leads/filter/', leads_filter_view.leads_filter, name="ledas_filter"),
    path('crm/leads/import/', lead_import_data_export_data.LeadImportView, name='lead_import'),
    path('import-progress/', lead_import_data_export_data.get_import_progress, name='import_progress'),
    path('crm/leads/export/', lead_import_data_export_data.export_leads_to_excel, name='export_leads'),
    path('crm/lead/comvert/coustomer/<int:id>/', convert_customer.convert_customer, name='convertocustomer'),

    # customer
    path('crm/coustomer/', customer_list_page.customer_page_view, name="coustomer"),
    path('crm/coustomer/<int:pk>/edit/',view_single_customer.view_sing_customer, name='editcustomer'),
    path('crm/coustomer/filter/', customer_filter.customer_filter, name="customers_filter"),
    path('crm/customer/import/', customer_import_data_and_export_data.customer_import_view, name='customer_import'),
    path('crm/customer/export/', customer_import_data_and_export_data.export_customer_data, name='export_customer'),

    # Setup functions
    path('new_country/', settings_view.new_countrys, name='new_country'),
    path('new_city/', settings_view.new_city, name='new_city'),
    path('new_referrals/', settings_view.new_referrals, name='new_referrals'),
    path('new_business_type/', settings_view.new_business_type, name='new_business_type'),

    # Reset Password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    # Bacic functions
    path('login/',login_page_view.login_page, name='login'),
    path('logout/', login_page_view.logout_page, name='logout_page'),
    path('darkmood/', basic_functions.darkmood, name='darkmood'),

    # Filter
    path('leads/thismonthleads/', leads_filter.thismonthleads, name='thismonthleads'),
    path('leads/last30days/', leads_filter.last30days, name='last30days'),
    path('leads/prospective_leads/', leads_filter.prospective_leads, name='prospective_leads'),
    path('leads/monthly_prospective/', leads_filter.monthly_prospective, name='monthly_prospective'),
    path('leads/last_30_days_prospective/', leads_filter.last_30_days_prospective, name='last_30_days_prospective'),
    path('leads/span_leads/', leads_filter.span_leads, name='span_leads'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)