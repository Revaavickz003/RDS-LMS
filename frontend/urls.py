from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from frontend.views import (
    crm_dashboard,
    lead_import_data_export_data,
    leads_list_page,
    settings_view,
    teamviewpage,
    calender_view,
    login_page_view,
    add_teams,
    reportspage,
    employees_views,
    employee_details_update_views,
    task_sheet_view,
    roles_views,
    deportments_views,
    employee_positions_views,
    view_single_lead,
    customer_views,
    single_employee_details_and_history,
    profile_view,
    customer_list_page,
    leads_filter_view,
    view_single_customer,
    customer_import_data_and_export_data,
    customer_filter,
    )

urlpatterns = [
    #  Login and Logout Views
    path('login/',login_page_view.login_page, name='login'),
    path('logout/', login_page_view.logout_page, name='logout_page'),
    path('activate/<uidb64>/<token>/', employees_views.activate_account, name='activate'),

    # sidebar Views
    path('', crm_dashboard.maindashbord_page_view, name="crmdashboard"),
    path('calendar/<int:year>/<int:month>/', calender_view.calendar_view, name='calendar'),
    path('calendar_view/', calender_view.calendar_view, name='calendar_view'),
    path('setting/', settings_view.setting, name='setting'),
    path('teamview/<str:teamname>/', teamviewpage.teamview, name="teamview"),
    path('profile/', profile_view.profile, name="profile_view"),
    
    #  Leads
    path('crm/leads/', leads_list_page.crm_page_view, name="leads"),
    path('crm/leads/<int:pk>/edit/',view_single_lead.view_sing_lead, name='editlead'),
    path('crm/leads/filter/', leads_filter_view.ledas_filter, name="ledas_filter"),
    path('crm/leads/import/', lead_import_data_export_data.LeadImportView, name='lead_import'),
    path('crm/leads/export/', lead_import_data_export_data.export_leads_to_excel, name='export_leads'),
    path('crm/lead/comvert/coustomer/<int:id>/', customer_views.convert_customer, name='convertocustomer'),

    # customer
    path('crm/coustomer/', customer_list_page.customer_page_view, name="coustomer"),
    path('crm/coustomer/<int:pk>/edit/',view_single_customer.view_sing_customer, name='editcustomer'),
    path('crm/coustomer/filter/', customer_filter.customers_filter, name="customers_filter"),
    path('crm/customer/import/', customer_import_data_and_export_data.customer_import_view, name='customer_import'),
    path('crm/customer/export/', customer_import_data_and_export_data.export_customer_data, name='export_customer'),

    # Employee 
    path('teamview/reports/<str:teamname>/', reportspage.reportsview, name="reportsview"),
    path('employees/', employees_views.employees, name='employees'),
    path('employees/<str:employeeid>/<str:employeename>/', single_employee_details_and_history.show_history, name='show_history'),
    path('employee_details_update/<int:pk>/', employee_details_update_views.employee_details_update, name='employee_details_update'),
    path('tasksheet/<str:user>/<str:date>/', task_sheet_view.task_sheet_function, name='task_sheet_function'),
    
    # Team Createt update  and delete
    path('addteams/', add_teams.addteams, name="addteams"),

    # Roles Created update  and delete 
    path('create_role/', roles_views.roles_create, name="create_role"),
    path('delete_role/<int:id>/', roles_views.roles_delete, name="delete_role"),
    path('update_role/<int:id>/', roles_views.roles_update, name="roles_update"),

    # Deporment Created update  and delete 
    path('create_deportment/', deportments_views.deportments_create, name="create_deportment"),
    path('delete_deportment/<int:id>/', deportments_views.deportments_delete, name="delete_deportment"),
    path('update_deportment/<int:id>/', deportments_views.deportments_update, name="update_deportments"),

    # Position Created update  and delete 
    path('create_position/', employee_positions_views.positions_create, name="create_position"),
    path('delete_position/<int:id>/', employee_positions_views.positions_delete, name="delete_position"),
    path('update_position/<int:id>/', employee_positions_views.positions_update, name="update_positions"),

    # Reset Password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)