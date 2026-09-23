def float_double_default_dtype(fn):
    @wraps(fn)
    def wrapped_fn(*args, **kwargs):
        cur_dtype = torch.get_default_dtype()
        try:
            torch.set_default_dtype(torch.float)
            fn(*args, **kwargs)
            torch.set_default_dtype(torch.double)
            fn(*args, **kwargs)
        finally:
            torch.set_default_dtype(cur_dtype)

    return wrapped_fn
