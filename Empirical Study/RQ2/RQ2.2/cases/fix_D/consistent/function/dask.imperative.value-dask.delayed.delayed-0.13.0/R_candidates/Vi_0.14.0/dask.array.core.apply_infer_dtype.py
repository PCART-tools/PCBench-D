def apply_infer_dtype(func, args, kwargs, funcname, suggest_dtype=True):
    args = [np.ones((1,) * x.ndim, dtype=x.dtype)
            if isinstance(x, Array) else x for x in args]
    try:
        o = func(*args, **kwargs)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = ''.join(traceback.format_tb(exc_traceback))
        suggest = ("Please specify the dtype explicitly using the "
                   "`dtype` kwarg.\n\n") if suggest_dtype else ""
        msg = ("`dtype` inference failed in `{0}`.\n\n"
               "{1}"
               "Original error is below:\n"
               "------------------------\n"
               "{2}\n\n"
               "Traceback:\n"
               "---------\n"
               "{3}").format(funcname, suggest, repr(e), tb)
    else:
        msg = None
    if msg is not None:
        raise ValueError(msg)
    return o.dtype
