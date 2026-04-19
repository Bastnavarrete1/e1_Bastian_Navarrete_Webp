from django.shortcuts import redirect
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_superuser:
            return redirect('inicio')

        return view_func(request, *args, **kwargs)

    return wrapper


def vendedor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if request.user.groups.filter(name="Vendedor").exists():
            return view_func(request, *args, **kwargs)

        return redirect('inicio')

    return wrapper