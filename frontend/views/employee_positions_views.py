from django.shortcuts import redirect
from frontend.models import Position
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def positions_create(request):
    if request.method == 'POST':
        if not Position.objects.filter(Position_Name=request.POST['newpositionname']).exists():
            Position.objects.create(Position_Name=request.POST['newpositionname'], created_by=request.user)
            messages.success(request, f"Position {request.POST['newpositionname']} Created Successfully")
            return redirect('setting')
        else:
            messages.error(request, f"This {request.POST['newpositionname']} is already taken.")
            return redirect('setting')
    else:
        messages.error(request,  "Invalid Request Method")
        return redirect('setting')
    
@login_required(login_url='/login')
def positions_update(request,id):
    if request.method == 'POST':
        update_positionname =  Position.objects.get(pk=id)
        update_positionname.Position_Name=request.POST['newpositionname']
        update_positionname.save()
        messages.warning(request,f"Position {update_positionname} as been updated successfuly")
        return redirect('setting')
    
@login_required(login_url='/login')
def positions_delete(request,id):
    delete_position =  Position.objects.get(pk=id)
    delete_position.delete()
    messages.warning(request,f"Position {delete_position.Position_Name} Deleted Successfully")
    return redirect('setting')
