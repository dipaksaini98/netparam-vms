from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_f):
    def wrapper_f(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home/')
        else:
            return view_f(request, *args, **kwargs)

    return wrapper_f


def allowed_users(allowed_roles=[]):
    def decorator(view_f):
        def wrapper_f(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_f(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allowed on this page!!")

        return wrapper_f
    return decorator


def admin_only(view_f):
    def wrapper_f(request, *args, **kwargs):
        return redirect('/employee_profile/')

    return wrapper_f
