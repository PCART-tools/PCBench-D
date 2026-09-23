def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False,
                columns=None, sparse=False, drop_first=False):
    """
    Convert categorical variable into dummy/indicator variables

    Parameters
    ----------
    data : array-like, Series, or DataFrame
    prefix : string, list of strings, or dict of strings, default None
        String to append DataFrame column names
        Pass a list with length equal to the number of columns
        when calling get_dummies on a DataFrame. Alternativly, `prefix`
        can be a dictionary mapping column names to prefixes.
    prefix_sep : string, default '_'
        If appending prefix, separator/delimiter to use. Or pass a
        list or dictionary as with `prefix.`
    dummy_na : bool, default False
        Add a column to indicate NaNs, if False NaNs are ignored.
    columns : list-like, default None
        Column names in the DataFrame to be encoded.
        If `columns` is None then all the columns with
        `object` or `category` dtype will be converted.
    sparse : bool, default False
        Whether the dummy columns should be sparse or not.  Returns
        SparseDataFrame if `data` is a Series or if all columns are included.
        Otherwise returns a DataFrame with some SparseBlocks.

        .. versionadded:: 0.16.1
    drop_first : bool, default False
        Whether to get k-1 dummies out of n categorical levels by removing the
        first level.

        .. versionadded:: 0.18.0
    Returns
    -------
    dummies : DataFrame or SparseDataFrame

    Examples
    --------
    >>> import pandas as pd
    >>> s = pd.Series(list('abca'))

    >>> pd.get_dummies(s)
       a  b  c
    0  1  0  0
    1  0  1  0
    2  0  0  1
    3  1  0  0

    >>> s1 = ['a', 'b', np.nan]

    >>> pd.get_dummies(s1)
       a  b
    0  1  0
    1  0  1
    2  0  0

    >>> pd.get_dummies(s1, dummy_na=True)
       a  b  NaN
    0  1  0    0
    1  0  1    0
    2  0  0    1

    >>> df = pd.DataFrame({'A': ['a', 'b', 'a'], 'B': ['b', 'a', 'c'],
                        'C': [1, 2, 3]})

    >>> pd.get_dummies(df, prefix=['col1', 'col2'])
       C  col1_a  col1_b  col2_a  col2_b  col2_c
    0  1       1       0       0       1       0
    1  2       0       1       1       0       0
    2  3       1       0       0       0       1

    >>> pd.get_dummies(pd.Series(list('abcaa')))
       a  b  c
    0  1  0  0
    1  0  1  0
    2  0  0  1
    3  1  0  0
    4  1  0  0

    >>> pd.get_dummies(pd.Series(list('abcaa')), drop_first=True))
       b  c
    0  0  0
    1  1  0
    2  0  1
    3  0  0
    4  0  0

    See Also
    --------
    Series.str.get_dummies
    """
    from pandas.tools.merge import concat
    from itertools import cycle

    if isinstance(data, DataFrame):
        # determine columns being encoded

        if columns is None:
            columns_to_encode = data.select_dtypes(
                include=['object', 'category']).columns
        else:
            columns_to_encode = columns

        # validate prefixes and separator to avoid silently dropping cols
        def check_len(item, name):
            length_msg = ("Length of '{0}' ({1}) did not match the length of "
                          "the columns being encoded ({2}).")

            if com.is_list_like(item):
                if not len(item) == len(columns_to_encode):
                    raise ValueError(length_msg.format(name, len(item),
                                                       len(columns_to_encode)))

        check_len(prefix, 'prefix')
        check_len(prefix_sep, 'prefix_sep')
        if isinstance(prefix, compat.string_types):
            prefix = cycle([prefix])
        if isinstance(prefix, dict):
            prefix = [prefix[col] for col in columns_to_encode]

        if prefix is None:
            prefix = columns_to_encode

        # validate separators
        if isinstance(prefix_sep, compat.string_types):
            prefix_sep = cycle([prefix_sep])
        elif isinstance(prefix_sep, dict):
            prefix_sep = [prefix_sep[col] for col in columns_to_encode]

        if set(columns_to_encode) == set(data.columns):
            with_dummies = []
        else:
            with_dummies = [data.drop(columns_to_encode, axis=1)]

        for (col, pre, sep) in zip(columns_to_encode, prefix, prefix_sep):

            dummy = _get_dummies_1d(data[col], prefix=pre, prefix_sep=sep,
                                    dummy_na=dummy_na, sparse=sparse,
                                    drop_first=drop_first)
            with_dummies.append(dummy)
        result = concat(with_dummies, axis=1)
    else:
        result = _get_dummies_1d(data, prefix, prefix_sep, dummy_na,
                                 sparse=sparse, drop_first=drop_first)
    return result
