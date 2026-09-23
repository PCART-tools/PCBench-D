def is_hashable(arg):
    """Return True if hash(arg) will succeed, False otherwise.

    Some types will pass a test against collections.Hashable but fail when they
    are actually hashed with hash().

    Distinguish between these and other types by trying the call to hash() and
    seeing if they raise TypeError.

    Examples
    --------
    >>> a = ([],)
    >>> isinstance(a, collections.Hashable)
    True
    >>> is_hashable(a)
    False
    """
    # unfortunately, we can't use isinstance(arg, collections.Hashable), which
    # can be faster than calling hash, because numpy scalars on Python 3 fail
    # this test

    # reconsider this decision once this numpy bug is fixed:
    # https://github.com/numpy/numpy/issues/5562

    try:
        hash(arg)
    except TypeError:
        return False
    else:
        return True
