from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def darkmood(request):
    messages.error(request, "Sorry, this is a premium function. If you wish to access it, please upgrade now.")
    return redirect('setting')