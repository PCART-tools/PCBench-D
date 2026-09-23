def str_cat(arr, others=None, sep=None, na_rep=None):
    """
    Concatenate strings in the Series/Index with given separator.

    Parameters
    ----------
    others : list-like, or list of list-likes
      If None, returns str concatenating strings of the Series
    sep : string or None, default None
    na_rep : string or None, default None
        If None, NA in the series are ignored.

    Returns
    -------
    concat : Series/Index of objects or str

    Examples
    --------
    When ``na_rep`` is `None` (default behavior), NaN value(s)
    in the Series are ignored.

    >>> Series(['a','b',np.nan,'c']).str.cat(sep=' ')
    'a b c'

    >>> Series(['a','b',np.nan,'c']).str.cat(sep=' ', na_rep='?')
    'a b ? c'

    If ``others`` is specified, corresponding values are
    concatenated with the separator. Result will be a Series of strings.

    >>> Series(['a', 'b', 'c']).str.cat(['A', 'B', 'C'], sep=',')
    0    a,A
    1    b,B
    2    c,C
    dtype: object

    Otherwise, strings in the Series are concatenated. Result will be a string.

    >>> Series(['a', 'b', 'c']).str.cat(sep=',')
    'a,b,c'

    Also, you can pass a list of list-likes.

    >>> Series(['a', 'b']).str.cat([['x', 'y'], ['1', '2']], sep=',')
    0    a,x,1
    1    b,y,2
    dtype: object
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
            if sep == '':
                na_rep = ''
            else:
                return sep.join(arr[notnull(arr)])
        return sep.join(np.where(mask, na_rep, arr))
