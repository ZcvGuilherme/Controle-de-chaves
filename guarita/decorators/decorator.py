from django.shortcuts import redirect
from functools import wraps

def require_pessoa(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, "pessoa"):
            return redirect("/admin/")
        return view_func(request, *args, **kwargs)
    return wrapper