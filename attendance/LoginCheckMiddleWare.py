from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


def role_redirect(request):
    if request.user.is_authenticated:
        if request.user.user_type == "1":
            return redirect('users:admin_home')
        elif request.user.user_type == "2":
            return redirect('users:hr_home')
        elif request.user.user_type == "3":
            return redirect('users:worker_home')
        else:
            return redirect('attendance:login')
    else:
        LoginCheckMiddleWare()


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        #  Check whether the user is logged in or not
        if user.is_authenticated:
            role_redirect(request)
        else:
            if request.path == reverse("attendance:login"):
                pass
            else:
                return redirect("attendance:login")
