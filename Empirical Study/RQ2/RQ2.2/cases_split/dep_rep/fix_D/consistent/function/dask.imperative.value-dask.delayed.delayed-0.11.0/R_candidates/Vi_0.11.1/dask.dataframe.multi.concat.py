def concat(dfs, axis=0, join='outer', interleave_partitions=False):
    """ Concatenate DataFrames along rows.

    - When axis=0 (default), concatenate DataFrames row-wise:

      - If all divisions are known and ordered, concatenate DataFrames keeping
        divisions. When divisions are not ordered, specifying
        interleave_partition=True allows concatenate divisions each by each.

      - If any of division is unknown, concatenate DataFrames resetting its
        division to unknown (None)

    - When axis=1, concatenate DataFrames column-wise:

      - Allowed if all divisions are known.

      - If any of division is unknown, it raises ValueError.

    Parameters
    ----------

    dfs : list
        List of dask.DataFrames to be concatenated
    axis : {0, 1, 'index', 'columns'}, default 0
        The axis to concatenate along
    join : {'inner', 'outer'}, default 'outer'
        How to handle indexes on other axis
    interleave_partitions : bool, default False
        Whether to concatenate DataFrames ignoring its order. If True, every
        divisions are concatenated each by each.

    Examples
    --------

    If all divisions are known and ordered, divisions are kept.

    >>> a                                               # doctest: +SKIP
    dd.DataFrame<x, divisions=(1, 3, 5)>
    >>> b                                               # doctest: +SKIP
    dd.DataFrame<y, divisions=(6, 8, 10)>
    >>> dd.concat([a, b])                               # doctest: +SKIP
    dd.DataFrame<concat-..., divisions=(1, 3, 6, 8, 10)>

    Unable to concatenate if divisions are not ordered.

    >>> a                                               # doctest: +SKIP
    dd.DataFrame<x, divisions=(1, 3, 5)>
    >>> b                                               # doctest: +SKIP
    dd.DataFrame<y, divisions=(2, 3, 6)>
    >>> dd.concat([a, b])                               # doctest: +SKIP
    ValueError: All inputs have known divisions which cannot be concatenated
    in order. Specify interleave_partitions=True to ignore order

    Specify interleave_partitions=True to ignore the division order.

    >>> dd.concat([a, b], interleave_partitions=True)   # doctest: +SKIP
    dd.DataFrame<concat-..., divisions=(1, 2, 3, 5, 6)>

    If any of division is unknown, the result division will be unknown

    >>> a                                               # doctest: +SKIP
    dd.DataFrame<x, divisions=(None, None)>
    >>> b                                               # doctest: +SKIP
    dd.DataFrame<y, divisions=(1, 4, 10)>
    >>> dd.concat([a, b])                               # doctest: +SKIP
    dd.DataFrame<concat-..., divisions=(None, None, None, None)>
    """
    if not isinstance(dfs, list):
        dfs = [dfs]
    if len(dfs) == 0:
        raise ValueError('Input must be a list longer than 0')
    if len(dfs) == 1:
        return dfs[0]

    if join not in ('inner', 'outer'):
        raise ValueError("'join' must be 'inner' or 'outer'")

    axis = DataFrame._validate_axis(axis)
    dasks = [df for df in dfs if isinstance(df, _Frame)]

    if all(df.known_divisions for df in dasks):
        dfs = _maybe_from_pandas(dfs)
        if axis == 1:
            return concat_indexed_dataframes(dfs, axis=axis, join=join)
        else:
            # must be converted here to check whether divisions can be
            # concatenated
            dfs = _maybe_from_pandas(dfs)
            # each DataFrame's division must be greater than previous one
            if all(dfs[i].divisions[-1] < dfs[i + 1].divisions[0]
                   for i in range(len(dfs) - 1)):
                name = 'concat-{0}'.format(tokenize(*dfs))
                dsk, meta = _concat_dfs(dfs, name, join=join)

                divisions = []
                for df in dfs[:-1]:
                    # remove last to concatenate with next
                    divisions += df.divisions[:-1]
                divisions += dfs[-1].divisions
                return new_dd_object(toolz.merge(dsk, *[df.dask for df in dfs]),
                                     name, meta, divisions)
            else:
                if interleave_partitions:
                    return concat_indexed_dataframes(dfs, join=join)

                raise ValueError('All inputs have known divisions which cannot '
                                 'be concatenated in order. Specify '
                                 'interleave_partitions=True to ignore order')
    elif (axis == 1 and
          len(dasks) == len(dfs) and
          all(not df.known_divisions for df in dfs) and
          len({df.npartitions for df in dasks}) == 1):
        warn("Concatenating dataframes with unknown divisions.\n"
             "We're assuming that the indexes of each dataframes are aligned\n."
             "This assumption is not generally safe.")
        return concat_unindexed_dataframes(dfs)

    else:
        if axis == 1:
            raise ValueError('Unable to concatenate DataFrame with unknown '
                             'division specifying axis=1')
        else:
            # concat will not regard Series as row
            dfs = _maybe_from_pandas(dfs)
            name = 'concat-{0}'.format(tokenize(*dfs))
            dsk, meta = _concat_dfs(dfs, name, join=join)

            divisions = [None] * (sum([df.npartitions for df in dfs]) + 1)
            return new_dd_object(toolz.merge(dsk, *[df.dask for df in dfs]),
                                 name, meta, divisions)
