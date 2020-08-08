from django.shortcuts import redirect


def login_register_check(view_func):
    def _is_logged_in(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return _is_logged_in


def superuser_check(view_func):
    def _is_superuer(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')

    return _is_superuer


def staff_check(view_func):
    def _is_staff(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')
    return _is_staff

#
# def cart_check(view_func):
#     def _is_cart(request, *args, **kwargs):
#
