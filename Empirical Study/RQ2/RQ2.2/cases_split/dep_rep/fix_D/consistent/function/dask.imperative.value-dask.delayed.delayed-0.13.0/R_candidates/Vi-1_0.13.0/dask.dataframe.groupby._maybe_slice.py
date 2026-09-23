def _maybe_slice(grouped, columns):
    """
    Slice columns if grouped is pd.DataFrameGroupBy
    """
    if isinstance(grouped, pd.core.groupby.DataFrameGroupBy):
        if columns is not None:
            if isinstance(columns, (tuple, list, set, pd.Index)):
                columns = list(columns)
            return grouped[columns]
    return grouped
