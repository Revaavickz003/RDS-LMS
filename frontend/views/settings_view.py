from django.shortcuts import  render, redirect
from frontend.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/login')
def setting(request):
    Users = CustomUser.objects.all()

    context = {
        'settings': 'activete',
        "Users": Users,
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

            # Get the ContentType instance for the Location model
            location_content_type = ContentType.objects.get_for_model(Location)
            
            new_activity = UserActivity.objects.create(
                user=request.user,
                timestamp=datetime.datetime.now(),
                lable=f"Create {Country_name} from country list",
                action="Created",
                content_type=location_content_type,
                object_id=new_country.pk,
            )
            new_activity.save()
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

            location_content_type = ContentType.objects.get_for_model(City)
            new_activity = UserActivity.objects.create(
                user=request.user,
                timestamp=datetime.datetime.now(),
                lable=f"Create {city_name} from city list",
                action="Created",
                content_type=location_content_type,
                object_id=city_name.pk,
            )
            new_activity.save()
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
            location_content_type = ContentType.objects.get_for_model(LeadTable)
            new_activity = UserActivity.objects.create(
                user=request.user,
                timestamp=datetime.datetime.now(),
                lable=f"Create {Referral_name} from referral list",
                action="Created",
                content_type=location_content_type,
                object_id=Referral_name.pk,
            )
            new_activity.save()
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
            location_content_type = ContentType.objects.get_for_model(OrgType)
            new_activity = UserActivity.objects.create(
                user=request.user,
                timestamp=datetime.datetime.now(),
                lable=f"Create {bussiness_type} from company type list",
                action="Created",
                content_type=location_content_type,
                object_id=bussiness_type.pk,
            )
            new_activity.save()
            messages.success(request, 'New company type Type Added Successfully')
        return redirect('setting')
    else:
        return redirect('setting')