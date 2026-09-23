def simps(y, x=None, dx=1.0, axis=-1, even=None):
    """An alias of `simpson`.

    `simps` is kept for backwards compatibility. For new code, prefer
    `simpson` instead.
    """
    return simpson(y, x=x, dx=dx, axis=axis, even=even)
