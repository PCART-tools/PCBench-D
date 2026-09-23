def str_translate(arr, table, deletechars=None):
    """
    Map all characters in the string through the given mapping table.
    Equivalent to standard :meth:`str.translate`. Note that the optional
    argument deletechars is only valid if you are using python 2. For python 3,
    character deletion should be specified via the table argument.

    Parameters
    ----------
    table : dict (python 3), str or None (python 2)
        In python 3, table is a mapping of Unicode ordinals to Unicode
        ordinals, strings, or None. Unmapped characters are left untouched.
        Characters mapped to None are deleted. :meth:`str.maketrans` is a
        helper function for making translation tables.
        In python 2, table is either a string of length 256 or None. If the
        table argument is None, no translation is applied and the operation
        simply removes the characters in deletechars. :func:`string.maketrans`
        is a helper function for making translation tables.
    deletechars : str, optional (python 2)
        A string of characters to delete. This argument is only valid
        in python 2.

    Returns
    -------
    translated : Series/Index of objects
    """
    if deletechars is None:
        f = lambda x: x.translate(table)
    else:
        from pandas import compat
        if compat.PY3:
            raise ValueError("deletechars is not a valid argument for "
                             "str.translate in python 3. You should simply "
                             "specify character deletions in the table "
                             "argument")
        f = lambda x: x.translate(table, deletechars)
    return _na_map(f, arr)
