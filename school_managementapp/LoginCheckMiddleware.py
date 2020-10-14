from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == '1':
                if modulename == 'school_managementapp.Hod_Views':
                    pass
                elif modulename == 'school_managementapp.views' or modulename == 'django.view.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('admin_home'))
            if user.user_type == '2':
                if modulename == 'school_managementapp.Staff_Views' or modulename == 'django.view.static':
                    pass
                elif modulename == 'school_managementapp.views':
                    pass
                else:
                    return HttpResponseRedirect('/staff_home')
            if user.user_type == '3':
                if modulename == 'school_managementapp.Student_Views' or modulename == 'django.view.static':
                    pass
                elif modulename == 'school_managementapp.views':
                    pass
                else:
                    return HttpResponseRedirect('/student_home')

        else:
            if request.path == reverse('showlogin') or request.path == reverse('dologin') or modulename == 'django.contrib.auth.views':
                pass
            else:
                return HttpResponseRedirect(reverse('showlogin'))



