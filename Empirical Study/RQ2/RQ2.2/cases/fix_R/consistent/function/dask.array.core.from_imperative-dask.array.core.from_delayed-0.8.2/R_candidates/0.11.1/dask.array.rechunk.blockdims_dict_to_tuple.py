def blockdims_dict_to_tuple(old, new):
    """

    >>> blockdims_dict_to_tuple((4, 5, 6), {1: 10})
    (4, 10, 6)
    """
    newlist = list(old)
    for k, v in new.items():
        newlist[k] = v
    return tuple(newlist)
