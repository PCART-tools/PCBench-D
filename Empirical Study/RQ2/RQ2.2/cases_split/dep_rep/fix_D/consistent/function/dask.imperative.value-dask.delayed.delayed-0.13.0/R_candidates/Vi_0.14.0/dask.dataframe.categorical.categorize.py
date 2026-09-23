def categorize(df, columns=None, index=None, **kwargs):
    """Convert columns of the DataFrame to category dtype.

    Parameters
    ----------
    columns : list, optional
        A list of column names to convert to categoricals. By default any
        column with an object dtype is converted to a categorical, and any
        unknown categoricals are made known.
    index : bool, optional
        Whether to categorize the index. By default, object indices are
        converted to categorical, and unknown categorical indices are made
        known. Set True to always categorize the index, False to never.
    kwargs
        Keyword arguments are passed on to compute.
    """
    if columns is None:
        columns = list(df.select_dtypes(['object', 'category']).columns)
    elif is_scalar(columns):
        columns = [columns]

    categories = [get_categories(df[col]) for col in columns]
    if index is False:
        index = None
    else:
        index = get_categories(df.index, index is None)

    # Compute the categories
    values = compute(index, *categories, **kwargs)
    categories = {c: v for (c, v) in zip(columns, values[1:]) if v is not None}

    # Nothing to do
    if not len(categories) and index is None:
        return df

    # Categorize each partition
    return df.map_partitions(_categorize_block, categories, values[0])
