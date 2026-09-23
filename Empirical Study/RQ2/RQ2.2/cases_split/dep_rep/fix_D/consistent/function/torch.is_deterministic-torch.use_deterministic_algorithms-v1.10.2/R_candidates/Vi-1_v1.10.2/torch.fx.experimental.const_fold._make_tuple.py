def _make_tuple(x):
    """
    Helper to convert x into a one item tuple if it's not a tuple already.
    """
    return x if isinstance(x, tuple) else (x,)
