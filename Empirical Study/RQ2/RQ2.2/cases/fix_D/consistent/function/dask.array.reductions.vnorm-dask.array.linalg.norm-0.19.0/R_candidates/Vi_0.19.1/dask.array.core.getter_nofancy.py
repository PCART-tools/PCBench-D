def getter_nofancy(a, b, asarray=True, lock=None):
    """ A simple wrapper around ``getter``.

    Used to indicate to the optimization passes that the backend doesn't
    support fancy indexing.
    """
    return getter(a, b, asarray=asarray, lock=lock)
