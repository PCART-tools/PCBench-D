def getter_inline(a, b, asarray=True, lock=None):
    """ A getter function that optimizations feel comfortable inlining

    Slicing operations with this function may be inlined into a graph, such as
    in the following rewrite

    **Before**

    >>> a = x[:10]  # doctest: +SKIP
    >>> b = a + 1  # doctest: +SKIP
    >>> c = a * 2  # doctest: +SKIP

    **After**

    >>> b = x[:10] + 1  # doctest: +SKIP
    >>> c = x[:10] * 2  # doctest: +SKIP

    This inlining can be relevant to operations when running off of disk.
    """
    return getter(a, b, asarray=asarray, lock=lock)
