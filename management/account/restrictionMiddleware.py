from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib import admin


class restrictionMiddleware(MiddlewareMixin):
    '''
    For restricting the user to view only pages they are supposed to
    '''

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename=="account.instructorviews":
                    return redirect('dashboard')
                elif modulename=="account.studentviews":
                    return redirect('dashboard')
                else:
                    pass
            elif user.user_type == "2":
                if modulename == "account.instructorviews":
                    pass
                elif modulename == "account.views":
                    pass
                else:
                    return redirect('insdashboard')
            elif user.user_type == "3":
                if modulename == "account.studentviews":
                    pass
                elif modulename == "account.views":
                    pass
                else:
                    return redirect('studashboard')
            else:
                return redirect('loginpage')

        else:
            if request.path == reverse("loginpage"):
                pass
            elif modulename=="django.contrib.admin.sites":
                pass
            else:
                return HttpResponseRedirect(reverse("loginpage"))