def merge(left, right, how='inner', on=None, left_on=None, right_on=None,
          left_index=False, right_index=False, suffixes=('_x', '_y'),
          npartitions=None, shuffle=None, max_branch=None):
    for o in [on, left_on, right_on]:
        if isinstance(o, _Frame):
            raise NotImplementedError(
                "Dask collections not currently allowed in merge columns")
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

    # Both sides indexed
    if (left_index and left.known_divisions and
            right_index and right.known_divisions):  # Do indexed join
        return join_indexed_dataframes(left, right, how=how,
                                       lsuffix=suffixes[0], rsuffix=suffixes[1])

    # Single partition on one side
    elif (left.npartitions == 1 and how in ('inner', 'right') or
          right.npartitions == 1 and how in ('inner', 'left')):
        return single_partition_join(left, right, how=how, right_on=right_on,
                left_on=left_on, left_index=left_index,
                right_index=right_index, suffixes=suffixes)

    # One side is indexed, the other not
    elif (left_index and left.known_divisions and not right_index or
          right_index and right.known_divisions and not left_index):
        left_empty = left._meta_nonempty
        right_empty = right._meta_nonempty
        meta = pd.merge(left_empty, right_empty, how=how, on=on,
                        left_on=left_on, right_on=right_on,
                        left_index=left_index, right_index=right_index,
                        suffixes=suffixes)
        if left_index and left.known_divisions:
            right = rearrange_by_divisions(right, right_on, left.divisions,
                    max_branch, shuffle=shuffle)
            left = left.clear_divisions()
        elif right_index and right.known_divisions:
            left = rearrange_by_divisions(left, left_on, right.divisions,
                    max_branch, shuffle=shuffle)
            right = right.clear_divisions()
        return map_partitions(pd.merge, left, right, meta=meta, how=how, on=on,
                left_on=left_on, right_on=right_on, left_index=left_index,
                right_index=right_index, suffixes=suffixes)
    # Catch all hash join
    else:
        return hash_join(left, left.index if left_index else left_on,
                         right, right.index if right_index else right_on,
                         how, npartitions, suffixes, shuffle=shuffle)
