from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.contrib import messages


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        print(request.user.profile.is_hrd)
        if not (request.user.profile.is_hrd or request.user.is_superuser):
            messages.warning(
                request, "ANDA TIDAK MEMILIKI IZIN MENGAKSES MENU TERSEBUT!")
            return redirect(reverse('home'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
