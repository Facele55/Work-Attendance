from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Permission
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from attendance.models import CustomUser


def hr_home(request):
    return render(request, "users/hr_templates/hr_home.html")


def admin_home(request):
    perm = Permission.objects.filter(user=request.user)
    context = {"perm": perm}
    return render(request, "users/admin_templates/admin_home.html", context)


def worker_home(request):
    return render(request, "users/worker_templates/worker_home.html")


def user_profile(request):
    c_user = CustomUser.objects.get(id=request.user.id)
    context = {"c_user": c_user}
    return render(request, 'users/base/profile.html', context)


def profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('users:profile')
    else:
        first_name = request.POST.get('first_name')
        print(first_name)
        last_name = request.POST.get('last_name')
        print(last_name)
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        rep_password = request.POST.get('repeat_password')
        print(rep_password)
        status = request.POST.get('status')
        #print(status)
        secret_word = request.POST.get('work_position')
        #print(secret_word)
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            #customuser.status = status
            #customuser.first_name = first_name
            #customuser.last_name = last_name
            #customuser.secret_word = secret_word
            #if password is not None and password != "":
            #    customuser.set_password(password)
            print(customuser)
            #customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('users:profile')
        except CustomUser.DoesNotExist:
            messages.error(request, "Failed to Update Profile")
            return redirect('users:profile')


class UpdatePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:update_password')
    template_name = 'users/base/change-password.html'
