from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from frontend.models import (
    CustomUser,
    Department,
    Position,
    TasksheetTable,
    Client,
    Lead,
    Team,
    Role,
    EmployeeStatus,
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
    list_display = ['org_name', 'client_name']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['Position_Name',]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_name',]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_name',]

@admin.register(TasksheetTable)
class TasksheetTableAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['assigned_by','assigned_to']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_name',]

@admin.register(EmployeeStatus)
class EmployeeStatusAdmin(admin.ModelAdmin):
    list_display = ['employee_id','status','created_date']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['client_id',]