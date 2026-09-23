def apply_infer_dtype(func, args, kwargs, funcname=None):
    args = [np.ones((1,) * x.ndim, dtype=x.dtype)
            if isinstance(x, Array) else x for x in args]
    try:
        o = func(*args, **kwargs)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = ''.join(traceback.format_tb(exc_traceback))
        msg = ("`dtype` inference failed{0}.\n\n"
               "Original error is below:\n"
               "------------------------\n"
               "{1}\n\n"
               "Traceback:\n"
               "---------\n"
               "{2}"
               ).format(" in `{0}`".format(funcname) if funcname else "",
                        repr(e), tb)
        raise ValueError(msg)
    return o.dtype
