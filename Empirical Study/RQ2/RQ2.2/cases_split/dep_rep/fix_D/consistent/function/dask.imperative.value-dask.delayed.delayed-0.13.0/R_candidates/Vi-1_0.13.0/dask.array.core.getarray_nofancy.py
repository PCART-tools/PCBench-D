def getarray_nofancy(a, b, lock=None):
    """ A simple wrapper around ``getarray``.

    Used to indicate to the optimization passes that the backend doesn't
    support "fancy indexing"
    """
    return getarray(a, b, lock=lock)
