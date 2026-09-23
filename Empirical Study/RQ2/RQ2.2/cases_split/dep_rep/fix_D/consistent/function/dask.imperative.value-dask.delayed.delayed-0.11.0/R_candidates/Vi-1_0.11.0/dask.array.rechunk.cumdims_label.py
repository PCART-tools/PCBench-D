def cumdims_label(chunks, const):
    """ Interal utility for cumulative sum with label.

    >>> cumdims_label(((5, 3, 3), (2, 2, 1)), 'n')  # doctest: +NORMALIZE_WHITESPACE
    [(('n', 0), ('n', 5), ('n', 8), ('n', 11)),
     (('n', 0), ('n', 2), ('n', 4), ('n', 5))]
    """
    return [tuple(zip((const,) * (1 + len(bds)),
                      list(accumulate(add, (0,) + bds))))
              for bds in chunks ]
