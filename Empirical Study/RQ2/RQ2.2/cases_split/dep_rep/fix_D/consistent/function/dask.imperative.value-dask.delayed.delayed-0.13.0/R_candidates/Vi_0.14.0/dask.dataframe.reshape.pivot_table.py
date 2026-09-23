def pivot_table(df, index=None, columns=None,
                values=None, aggfunc='mean'):
    """
    Create a spreadsheet-style pivot table as a DataFrame. Target ``columns``
    must have category dtype to infer result's ``columns``.
    ``index``, ``columns``, ``values`` and ``aggfunc`` must be all scalar.

    Parameters
    ----------
    data : DataFrame
    values : scalar
        column to aggregate
    index : scalar
        column to be index
    columns : scalar
        column to be columns
    aggfunc : {'mean', 'sum', 'count'}, default 'mean'

    Returns
    -------
    table : DataFrame
    """

    if not is_scalar(index) or index is None:
        raise ValueError("'index' must be the name of an existing column")
    if not is_scalar(columns) or columns is None:
        raise ValueError("'columns' must be the name of an existing column")
    if not is_categorical_dtype(df[columns]):
        raise ValueError("'columns' must be category dtype")
    if not has_known_categories(df[columns]):
        raise ValueError("'columns' must have known categories. Please use "
                         "`df[columns].cat.as_known()` beforehand to ensure "
                         "known categories")
    if not is_scalar(values) or values is None:
        raise ValueError("'values' must be the name of an existing column")
    if not is_scalar(aggfunc) or aggfunc not in ('mean', 'sum', 'count'):
        raise ValueError("aggfunc must be either 'mean', 'sum' or 'count'")

    # _emulate can't work for empty data
    # the result must have CategoricalIndex columns
    new_columns = pd.CategoricalIndex(df[columns].cat.categories, name=columns)
    meta = pd.DataFrame(columns=new_columns, dtype=np.float64)

    kwargs = {'index': index, 'columns': columns, 'values': values}

    pv_sum = apply_concat_apply([df],
                                chunk=methods.pivot_sum,
                                aggregate=methods.pivot_agg,
                                meta=meta,
                                token='pivot_table_sum',
                                chunk_kwargs=kwargs)
    pv_count = apply_concat_apply([df],
                                  chunk=methods.pivot_count,
                                  aggregate=methods.pivot_agg,
                                  meta=meta,
                                  token='pivot_table_count',
                                  chunk_kwargs=kwargs)

    if aggfunc == 'sum':
        return pv_sum
    elif aggfunc == 'count':
        return pv_count
    elif aggfunc == 'mean':
        return pv_sum / pv_count
    else:
        raise ValueError
