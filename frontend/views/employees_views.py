from django.shortcuts import render, redirect
from frontend.models import *
from django.contrib.auth.hashers import make_password
import random
import string
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator  # Add this import

# Function to generate a random password
def generate_random_password(length=18):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# View function to handle employee creation
@login_required(login_url='/login')
def employees(request):
    if request.method == 'POST':
        # Handle file uploads separately
        employee_photo = request.FILES.get('employee_photo', None)
        document = request.FILES.get('document', None)

        try:
            role = Role.objects.get(pk=int(request.POST['role']))
        except (Role.DoesNotExist, KeyError):
            role = None
        try:
            department = Department.objects.get(pk=int(request.POST['department']))
        except (Department.DoesNotExist, KeyError):
            department = None 
        try:
            position = Position.objects.get(pk=int(request.POST['position']))
        except (Position.DoesNotExist, KeyError):
            position = None

        # Convert string inputs to boolean values
        is_trainee = request.POST.get('is_trainee', '') == 'Yes'
        is_staff = request.POST.get('is_staff', '') == 'Yes'
        is_teamlead = request.POST.get('is_teamlead', '') == 'Yes'
        is_admin = request.POST.get('is_admin', '') == 'Yes'

        # Create a new CustomUser object
        new_employee = CustomUser.objects.create(
            username=request.POST['username'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            employee_mobile_number=request.POST['employee_mobile_number'],
            role=role,
            department=department,
            position=position,
            date_of_birth=request.POST['date_of_birth'],
            parent_number=request.POST['parent_number'],
            qualification=request.POST['qualification'],
            company_email=request.POST['company_email'],
            date_of_join=request.POST['date_of_join'],
            is_trainee=is_trainee,
            is_staff=is_staff,
            is_teamlead=is_teamlead,
            is_admin=is_admin,
            address=request.POST['address'],
            employee_photo=employee_photo,
            document=document,
        )

        # Generate and set a random password
        password = generate_random_password()
        new_employee.set_password(password)
        new_employee.save()


        return redirect('employees')

    # Retrieve all users, roles, positions, and departments for rendering the template
    ALL_users = CustomUser.objects.all()[::-1]
    Roles = Role.objects.all() 
    Positions = Position.objects.all()
    Departments = Department.objects.all()
    context = {
        'Employees': 'activete',
        'ALL_users': ALL_users,
        'Roles': Roles,
        'Positions': Positions,
        'Departments': Departments,
        "Teams": Team.objects.all(),
    }

    return render(request, 'Revaa/employees_page.html', context)

from django.http import HttpResponse

def activate_account(request, uidb64, token):
    # Your activation logic goes here
    return HttpResponse("Activation logic goes here")