def cumtrapz(y, x=None, dx=1.0, axis=-1, initial=None):
    """`An alias of `cumulative_trapezoid`.

    `cumtrapz` is kept for backwards compatibility. For new code, prefer
    `cumulative_trapezoid` instead.
    """
    return cumulative_trapezoid(y, x=x, dx=dx, axis=axis, initial=initial)
