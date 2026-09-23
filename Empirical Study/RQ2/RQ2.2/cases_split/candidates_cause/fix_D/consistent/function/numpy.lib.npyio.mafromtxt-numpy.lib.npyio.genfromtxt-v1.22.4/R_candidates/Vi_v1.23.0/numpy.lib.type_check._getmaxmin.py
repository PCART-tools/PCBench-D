def _getmaxmin(t):
    from numpy.core import getlimits
    f = getlimits.finfo(t)
    return f.max, f.min
