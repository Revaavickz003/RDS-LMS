from django.shortcuts import redirect
from frontend.models import Department
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def deportments_create(request):
    if request.method == 'POST':
        if not Department.objects.filter(department_name=request.POST['deportmentname']).exists():
            Department.objects.create(department_name=request.POST['deportmentname'], created_by=request.user)
            messages.success(request, "Department Created Successfully")
            return redirect('setting')
        else:
            messages.error(request, f"This {request.POST['deportmentname']} is already taken.")
            return redirect('setting')
    else:
        messages.error(request,  "Invalid Request Method")
        return redirect('setting')
    
@login_required(login_url='/login')
def deportments_update(request,id):
    if request.method == 'POST':
        update_deportmentname =  Department.objects.get(pk=id)
        update_deportmentname.department_name=request.POST['deportmentname']
        update_deportmentname.save()
        messages.warning(request,f"Deportment {update_deportmentname} as been updated successfuly")
        return redirect('setting')
    
@login_required(login_url='/login')
def deportments_delete(request,id):
    delete_deportment =  Department.objects.get(pk=id)
    delete_deportment.delete()
    messages.warning(request,f"Deportment {delete_deportment.department_name} Deleted Successfully")
    return redirect('setting')
