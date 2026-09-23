def _maybe_slice(grouped, columns):
    """
    Slice columns if grouped is pd.DataFrameGroupBy
    """
    if isinstance(grouped, pd.core.groupby.DataFrameGroupBy):
        if columns is not None:
            columns = columns if isinstance(columns, str) else list(columns)
            return grouped[columns]
    return grouped
