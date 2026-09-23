def robust_wraps(wrapper):
    """ A weak version of wraps that only copies doc """
    def _(wrapped):
        wrapped.__doc__ = wrapper.__doc__
        return wrapped
    return _
