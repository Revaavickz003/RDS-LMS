from django.shortcuts import render, redirect
from frontend.models import Role, Department, Position, CustomUser
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def employee_details_update(request, pk):
    if request.method == 'POST':
        # Handle file uploads separately
        employee_photo = request.FILES.get('employee_photo')
        
        try:
            role = Role.objects.get(pk=int(request.POST.get('role', '')))
        except (Role.DoesNotExist, ValueError):
            role = None
        
        try:
            department = Department.objects.get(pk=int(request.POST.get('department', '')))
        except (Department.DoesNotExist, ValueError):
            department = None 
        
        try:
            position = Position.objects.get(pk=int(request.POST.get('position', '')))
        except (Position.DoesNotExist, ValueError):
            position = None

        is_trainee = request.POST.get('is_trainee', '') == 'Yes'
        is_staff = request.POST.get('is_staff', '') == 'Yes'
        is_teamlead = request.POST.get('is_teamlead', '') == 'Yes'
        is_admin = request.POST.get('is_admin', '') == 'Yes'
        is_active = request.POST.get('is_active', '') == 'Yes'

        emp = CustomUser.objects.get(pk=pk)
        emp.first_name = request.POST.get('first_name', '')
        emp.last_name = request.POST.get('last_name', '')
        emp.email = request.POST.get('email', '')
        emp.employee_mobile_number = request.POST.get('employee_mobile_number', '')
        emp.role = role
        emp.department = department
        emp.position = position
        emp.date_of_birth = request.POST.get('date_of_birth', '')
        emp.parent_number = request.POST.get('parent_number', '')
        emp.employee_photo = employee_photo
        emp.qualification = request.POST.get('qualification', '')
        emp.company_email = request.POST.get('company_email', '')
        emp.date_of_join = request.POST.get('date_of_join', '')
        emp.is_active = is_active
        emp.is_trainee = is_trainee
        emp.is_staff = is_staff
        emp.is_teamlead = is_teamlead
        emp.is_admin = is_admin
        emp.address = request.POST.get('address', '')

        emp.save()
        print("Employee details updated successfully")

    return redirect('employees')
