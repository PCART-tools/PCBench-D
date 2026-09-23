def trace_args(func):
    def tofloat(x):
        if isinstance(x, mpmath.mpc):
            return complex(x)
        else:
            return float(x)

    def wrap(*a, **kw):
        sys.stderr.write("%r: " % (tuple(map(tofloat, a)),))
        sys.stderr.flush()
        try:
            r = func(*a, **kw)
            sys.stderr.write("-> %r" % r)
        finally:
            sys.stderr.write("\n")
            sys.stderr.flush()
        return r
    return wrap
