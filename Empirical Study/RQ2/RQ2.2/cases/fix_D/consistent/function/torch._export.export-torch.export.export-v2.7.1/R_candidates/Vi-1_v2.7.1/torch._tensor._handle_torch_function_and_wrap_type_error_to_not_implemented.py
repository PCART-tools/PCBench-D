def _handle_torch_function_and_wrap_type_error_to_not_implemented(f):
    assigned = functools.WRAPPER_ASSIGNMENTS

    @functools.wraps(f, assigned=assigned)
    def wrapped(*args, **kwargs):
        try:
            # See https://github.com/pytorch/pytorch/issues/75462
            if has_torch_function(args):
                return handle_torch_function(wrapped, args, *args, **kwargs)
            return f(*args, **kwargs)
        except TypeError:
            return NotImplemented

    return wrapped
