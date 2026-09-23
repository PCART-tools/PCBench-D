def is_list_of_ints(intlist):
    """Return True if list is a list of ints.

    .. deprecated:: 2.6
        This is deprecated and will be removed in NetworkX v3.0.
    """
    msg = (
        "is_list_of_ints is deprecated and will be removed in 3.0."
        "See also: ``networkx.utils.make_list_of_ints.``"
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)
    if not isinstance(intlist, list):
        return False
    for i in intlist:
        if not isinstance(i, int):
            return False
    return True
