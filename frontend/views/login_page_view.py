from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from frontend.models import CustomUser
from django.contrib.auth.decorators import login_required

def login_page(request):
    if request.user.is_authenticated:
        return redirect('crmdashboard')  # Redirect to main dashboard if user is already logged in

    if request.method == 'POST':
        email_or_username = request.POST.get('emailinput')
        password = request.POST.get('passwordinput')

        user = authenticate(request, username=email_or_username, password=password)

        if user is not None:
            login(request, user)
            return redirect('crmdashboard') 
        else:
            messages.error(request, 'Invalid email/username or password. Please try again.')

    return render(request, 'Revaa/loginpage.html') 

@login_required
def logout_page(request):
    logout(request)
    return redirect('login')
