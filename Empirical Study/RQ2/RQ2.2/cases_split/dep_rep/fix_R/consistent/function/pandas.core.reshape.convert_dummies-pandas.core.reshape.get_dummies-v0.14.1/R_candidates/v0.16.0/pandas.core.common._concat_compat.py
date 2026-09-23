def _concat_compat(to_concat, axis=0):
    """
    provide concatenation of an array of arrays each of which is a single
    'normalized' dtypes (in that for example, if its object, then it is a non-datetimelike
    provde a combined dtype for the resulting array the preserves the overall dtype if possible)

    Parameters
    ----------
    to_concat : array of arrays
    axis : axis to provide concatenation

    Returns
    -------
    a single array, preserving the combined dtypes
    """

    # filter empty arrays
    # 1-d dtypes always are included here
    def is_nonempty(x):
        try:
            return x.shape[axis] > 0
        except Exception:
            return True
    nonempty = [x for x in to_concat if is_nonempty(x)]

    # If all arrays are empty, there's nothing to convert, just short-cut to
    # the concatenation, #3121.
    #
    # Creating an empty array directly is tempting, but the winnings would be
    # marginal given that it would still require shape & dtype calculation and
    # np.concatenate which has them both implemented is compiled.

    typs = get_dtype_kinds(to_concat)

    # these are mandated to handle empties as well
    if 'datetime' in typs or 'timedelta' in typs:
        from pandas.tseries.common import _concat_compat
        return _concat_compat(to_concat, axis=axis)

    elif 'sparse' in typs:
        from pandas.sparse.array import _concat_compat
        return _concat_compat(to_concat, axis=axis)

    elif 'category' in typs:
        from pandas.core.categorical import _concat_compat
        return _concat_compat(to_concat, axis=axis)

    if not nonempty:

        # we have all empties, but may need to coerce the result dtype to object if we
        # have non-numeric type operands (numpy would otherwise cast this to float)
        typs = get_dtype_kinds(to_concat)
        if len(typs) != 1:

            if not len(typs-set(['i','u','f'])) or not len(typs-set(['bool','i','u'])):
                # let numpy coerce
                pass
            else:
                # coerce to object
                to_concat = [ x.astype('object') for x in to_concat ]

    return np.concatenate(to_concat,axis=axis)
