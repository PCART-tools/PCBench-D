def _silence_fp_errors(func):
    # warning: don't apply to test_ functions as is, then those will be skipped
    def wrap(*a, **kw):
        olderr = np.seterr(all='ignore')
        try:
            return func(*a, **kw)
        finally:
            np.seterr(**olderr)
    wrap.__name__ = func.__name__
    return wrap
