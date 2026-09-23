def blockshape_dict_to_tuple(old_chunks, d):
    """

    >>> blockshape_dict_to_tuple(((4, 4), (5, 5)), {1: 3})
    ((4, 4), (3, 3, 3, 1))
    """
    shape = tuple(map(sum, old_chunks))
    new_chunks = list(old_chunks)
    for k, v in d.items():
        div = shape[k] // v
        mod = shape[k] % v
        new_chunks[k] = (v,) * div + ((mod,) if mod else ())
    return tuple(new_chunks)
