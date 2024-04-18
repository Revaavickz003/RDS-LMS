from django.shortcuts import  render, redirect
from frontend.models import Role
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def roles_create(request):
    if request.method == 'POST':
        Role.objects.create(role_name=request.POST['rolename'], is_active=True, created_by=request.user)
        messages.success(request, "Role Created Successfully")
        return redirect('setting')
    else:
        messages.error(request,  "Invalid Request Method")
        return redirect('setting')
    
@login_required(login_url='/login')
def roles_update(request,id):
    if request.method == 'POST':
        update_role =  Role.objects.get(pk=id)
        update_role.role_name=request.POST['rolename']
        update_role.save()
        messages.warning(request,"Role as been updated successfuly")
        return redirect('setting')
    
@login_required(login_url='/login')
def roles_delete(request,id):
    delete_role =  Role.objects.get(pk=id)
    delete_role.delete()
    messages.warning(request,"Role Deleted Successfully")
    return redirect('setting')
