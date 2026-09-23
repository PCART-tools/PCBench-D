def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False,
                columns=None, sparse=False, drop_first=False):
    """
    Convert categorical variable into dummy/indicator variables. Data must
    have category dtype to infer result's ``columns``

    Parameters
    ----------
    data : Series or DataFrame with category dtype
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
        `category` dtype will be converted.
    drop_first : bool, default False
        Whether to get k-1 dummies out of k categorical levels by removing the
        first level.
    Returns
    -------
    dummies : DataFrame
    """

    if isinstance(data, (pd.Series, pd.DataFrame)):
        return pd.get_dummies(data, prefix=prefix,
                              prefix_sep=prefix_sep, dummy_na=dummy_na,
                              columns=columns, sparse=sparse,
                              drop_first=drop_first)

    not_cat_msg = ("`get_dummies` with non-categorical dtypes is not "
                   "supported. Please use `df.categorize()` beforehand to "
                   "convert to categorical dtype.")

    unknown_cat_msg = ("`get_dummies` with unknown categories is not "
                       "supported. Please use `column.cat.as_known()` or "
                       "`df.categorize()` beforehand to ensure known "
                       "categories")

    if isinstance(data, Series):
        if not is_categorical_dtype(data):
            raise NotImplementedError(not_cat_msg)
        if not has_known_categories(data):
            raise NotImplementedError(unknown_cat_msg)
    elif isinstance(data, DataFrame):
        if columns is None:
            if (data.dtypes == 'object').any():
                raise NotImplementedError(not_cat_msg)
            columns = data._meta.select_dtypes(include=['category']).columns
        else:
            if not all(is_categorical_dtype(data[c]) for c in columns):
                raise NotImplementedError(not_cat_msg)

        if not all(has_known_categories(data[c]) for c in columns):
            raise NotImplementedError(unknown_cat_msg)

    if sparse:
        raise NotImplementedError('sparse=True is not supported')

    return map_partitions(pd.get_dummies, data, prefix=prefix,
                          prefix_sep=prefix_sep, dummy_na=dummy_na,
                          columns=columns, sparse=sparse,
                          drop_first=drop_first)
