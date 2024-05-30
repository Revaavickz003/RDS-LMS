from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from frontend.models import (
    CustomUser,
    Lead,
    OrgType, 
    Location, 
    City,
    ProductTable,
    LeadTable,
    customertable,
    OrgName,
    UserActivity,
)

admin.site.register(OrgType)
admin.site.register(OrgName)
admin.site.register(Location)
admin.site.register(City)
admin.site.register(ProductTable)
admin.site.register(LeadTable)
admin.site.register(customertable)
admin.site.register(UserActivity)

@admin.register(CustomUser)
class CustomuserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['username', 'first_name']

@admin.register(Lead)
class LeadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['company_name', 'client_name']
