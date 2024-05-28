from django.shortcuts import  render, redirect
from frontend.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/login')
def setting(request):
    Roles = Role.objects.all()
    Departments = Department.objects.all()
    Positions = Position.objects.all()
    Users = CustomUser.objects.all()
    Teams = Team.objects.all()

    context = {
        'settings': 'activete',
        "Roles": Roles,
        "Departments": Departments,
        "Positions": Positions,
        "Users": Users,
        "Teams":Teams,
        "countrys":Location.objects.all(),
        "citys":City.objects.all(),
        "Referrals":LeadTable.objects.all(),
        "bussiness_types":OrgType.objects.all(),
    }
    return render(request, 'Revaa/setting_page.html', context)

@login_required(login_url='/login')
def new_countrys(request):
    if request.method == 'POST':
        Country_name = request.POST.get('Country_name')
        if Location.objects.filter(location=Country_name).exists():
            messages.error(request, 'Country Already Exists')
        else:
            new_country = Location.objects.create(location=Country_name)
            new_country.save()
            messages.success(request, 'Country Added Successfully')
        return redirect('setting')
    else:
        return redirect('setting')
    
@login_required(login_url='/login')
def new_city(request):
    if request.method == 'POST':
        city_name = request.POST.get('city_name')
        if City.objects.filter(city=city_name).exists():
            messages.error(request, 'City Already Exists')
        else:
            city_name = City.objects.create(city=city_name)
            city_name.save()
            messages.success(request, 'City Added Successfully')
        return redirect('setting')
    else:
        return redirect('setting')
    
@login_required(login_url='/login')
def new_referrals(request):
    if request.method == 'POST':
        Referral_name = request.POST.get('Referral_name')
        if LeadTable.objects.filter(Lead_Name=Referral_name).exists():
            messages.error(request, 'Referral Name Already Exists')
        else:
            Referral_name = LeadTable.objects.create(Lead_Name=Referral_name)
            Referral_name.save()
            messages.success(request, 'New Referral Added Successfully')
        return redirect('setting')
    else:
        return redirect('setting')
    
@login_required(login_url='/login')
def new_business_type(request):
    if request.method == 'POST':
        bussiness_type = request.POST.get('bussiness_type')
        if OrgType.objects.filter(org_type=bussiness_type).exists():
            messages.error(request, 'Bussiness Type Already Exists')
        else:
            bussiness_type = OrgType.objects.create(org_type=bussiness_type)
            bussiness_type.save()
            messages.success(request, 'New Bussiness Type Added Successfully')
        return redirect('setting')
    else:
        return redirect('setting')