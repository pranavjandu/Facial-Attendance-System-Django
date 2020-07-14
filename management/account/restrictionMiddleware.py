from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class restrictionMiddleware(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "account.adminviews":
                    pass
                elif modulename == "account.views":
                    pass
                else:
                    return redirect('dashboard')
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
            else:
                return HttpResponseRedirect(reverse("loginpage"))