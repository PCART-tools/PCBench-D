def str_cat(arr, others=None, sep=None, na_rep=None):
    """
    Concatenate arrays of strings with given separator

    Parameters
    ----------
    arr : list or array-like
    others : list or array, or list of arrays
    sep : string or None, default None
    na_rep : string or None, default None
        If None, an NA in any array will propagate

    Returns
    -------
    concat : array
    """
    if sep is None:
        sep = ''

    if others is not None:
        arrays = _get_array_list(arr, others)

        n = _length_check(arrays)
        masks = np.array([isnull(x) for x in arrays])
        cats = None

        if na_rep is None:
            na_mask = np.logical_or.reduce(masks, axis=0)

            result = np.empty(n, dtype=object)
            np.putmask(result, na_mask, np.nan)

            notmask = ~na_mask

            tuples = zip(*[x[notmask] for x in arrays])
            cats = [sep.join(tup) for tup in tuples]

            result[notmask] = cats
        else:
            for i, x in enumerate(arrays):
                x = np.where(masks[i], na_rep, x)
                if cats is None:
                    cats = x
                else:
                    cats = cats + sep + x

            result = cats

        return result
    else:
        arr = np.asarray(arr, dtype=object)
        mask = isnull(arr)
        if na_rep is None and mask.any():
            return np.nan
        return sep.join(np.where(mask, na_rep, arr))
