def _call_method(method, rref, *args, **kwargs):
    return method(rref.local_value(), *args, **kwargs)
