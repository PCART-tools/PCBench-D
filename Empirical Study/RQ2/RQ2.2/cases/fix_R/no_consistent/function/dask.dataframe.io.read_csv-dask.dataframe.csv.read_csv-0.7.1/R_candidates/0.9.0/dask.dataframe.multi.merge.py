def merge(left, right, how='inner', on=None, left_on=None, right_on=None,
          left_index=False, right_index=False, suffixes=('_x', '_y'),
          npartitions=None):

    if not on and not left_on and not right_on and not left_index and not right_index:
        on = [c for c in left.columns if c in right.columns]
        if not on:
            left_index = right_index = True

    if on and not left_on and not right_on:
        left_on = right_on = on
        on = None

    if (isinstance(left, (pd.Series, pd.DataFrame)) and
        isinstance(right, (pd.Series, pd.DataFrame))):
        return pd.merge(left, right, how=how, on=on, left_on=left_on,
                        right_on=right_on, left_index=left_index,
                        right_index=right_index, suffixes=suffixes)

    # Transform pandas objects into dask.dataframe objects
    if isinstance(left, (pd.Series, pd.DataFrame)):
        if right_index and left_on:  # change to join on index
            left = left.set_index(left[left_on])
            left_on = False
            left_index = True
        left = from_pandas(left, npartitions=1)  # turn into DataFrame

    if isinstance(right, (pd.Series, pd.DataFrame)):
        if left_index and right_on:  # change to join on index
            right = right.set_index(right[right_on])
            right_on = False
            right_index = True
        right = from_pandas(right, npartitions=1)  # turn into DataFrame

    # Both sides are now dd.DataFrame or dd.Series objects

    if left_index and right_index:  # Do indexed join
        return join_indexed_dataframes(left, right, how=how,
                                       lsuffix=suffixes[0], rsuffix=suffixes[1])

    else:                           # Do hash join
        return hash_join(left, left.index if left_index else left_on,
                         right, right.index if right_index else right_on,
                         how, npartitions, suffixes)
