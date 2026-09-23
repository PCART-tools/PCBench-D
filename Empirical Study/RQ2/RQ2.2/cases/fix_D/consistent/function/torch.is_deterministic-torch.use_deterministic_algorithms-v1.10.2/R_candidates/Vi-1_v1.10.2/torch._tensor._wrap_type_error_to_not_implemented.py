def _wrap_type_error_to_not_implemented(f):
    # functools.wraps doesn't work well with methods in python 2
    method_assignments = ('__name__', '__doc__')
    assigned = functools.WRAPPER_ASSIGNMENTS

    @functools.wraps(f, assigned=assigned)
    def wrapped(*args, **kwargs):
        if has_torch_function(args):
            return handle_torch_function(wrapped, args, *args, **kwargs)
        try:
            return f(*args, **kwargs)
        except TypeError:
            return NotImplemented
    return wrapped
