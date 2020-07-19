

from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.

def loginpage(request):
    '''
    For logging users in
    '''
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)  #django default authentication
        if user is not None:
            login(request,user)
            if user.user_type=='1':
                return redirect('dashboard')
            elif user.user_type=='2':
                return redirect('insdashboard')
            elif user.user_type=='3':
                return redirect('studashboard')
        else:
            messages.info(request," Wrong Credentials! Please Try again or contact your administrator")

    return render(request,'login.html')




def logoutUser(request):
    '''
    for logging user out and redirecting to login-page
    '''
    logout(request)
    return redirect('loginpage')




