@disallow('M8','m8')
@bottleneck_switch(ddof=1)
def nanvar(values, axis=None, skipna=True, ddof=1):

    # we are going to allow timedelta64[ns] here
    # but NOT going to coerce them to the Timedelta type
    # as this could cause overflow
    # so var cannot be computed (but std can!)
    return _nanvar(values, axis=axis, skipna=skipna, ddof=ddof)
