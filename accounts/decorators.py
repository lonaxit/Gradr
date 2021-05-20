from django.http import HttpResponse
from django.shortcuts import redirect


# the first decorator stops a user accessing login and register pages
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('admin')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                # group = request.user.groups.all()[0].name
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('access denied')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():

            group = request.user.groups.all()[0].name

        if group == 'customer':
            return HttpResponse('Iam a customer')
        if group == 'student':
            return redirect('student')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_function
