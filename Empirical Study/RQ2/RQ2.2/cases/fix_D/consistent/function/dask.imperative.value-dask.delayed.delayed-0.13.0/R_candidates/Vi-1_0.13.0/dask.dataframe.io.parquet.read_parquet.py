def read_parquet(path, columns=None, filters=None, categories=None, index=None,
                 storage_options=None):
    """
    Read ParquetFile into a Dask DataFrame

    This reads a directory of Parquet data into a Dask.dataframe, one file per
    partition.  It selects the index among the sorted columns if any exist.

    This uses the fastparquet project: http://fastparquet.readthedocs.io/en/latest

    Parameters
    ----------
    path : string
        Source directory for data.
        Prepend with protocol like ``s3://`` or ``hdfs://`` for remote data.
    columns: list or None
        List of column names to load
    filters: list
        List of filters to apply, like ``[('x', '>' 0), ...]``
    index: string or None
        Name of index column to use if that column is sorted
    categories: list or None
        For any fields listed here, if the parquet encoding is Dictionary,
        the column will be created with dtype category. Use only if it is
        guaranteed that the column is encoded as dictionary in all row-groups.
    storage_options : dict
        Key/value pairs to be passed on to the file-system backend, if any.

    Examples
    --------
    >>> df = read_parquet('s3://bucket/my-parquet-data')  # doctest: +SKIP

    See Also
    --------
    to_parquet
    """
    if fastparquet is False:
        raise ImportError("fastparquet not installed")
    if filters is None:
        filters = []
    myopen = OpenFileCreator(path, compression=None, text=False,
                             **(storage_options or {}))

    if isinstance(columns, list):
        columns = tuple(columns)

    try:
        pf = fastparquet.ParquetFile(path + myopen.fs.sep + '_metadata',
                                     open_with=myopen,
                                     sep=myopen.fs.sep)
    except:
        pf = fastparquet.ParquetFile(path, open_with=myopen, sep=myopen.fs.sep)

    name = 'read-parquet-' + tokenize(pf, columns, categories)

    rgs = [rg for rg in pf.row_groups if
           not(fastparquet.api.filter_out_stats(rg, filters, pf.helper)) and
           not(fastparquet.api.filter_out_cats(rg, filters))]

    # get category values from first row-group
    categories = categories or []
    cats = pf.grab_cats(categories)
    categories = [cat for cat in categories if cats.get(cat, None) is not None]

    # Find an index among the partially sorted columns
    minmax = fastparquet.api.sorted_partitioned_columns(pf)

    if index is False:
        index_col = None
    elif len(minmax) == 1:
        index_col = first(minmax)
    elif len(minmax) > 1:
        if index:
            index_col = index
        elif 'index' in minmax:
            index_col = 'index'
        else:
            raise ValueError("Multiple possible indexes exist: %s.  "
                             "Please select one with index='index-name'"
                             % sorted(minmax))
    else:
        index_col = None

    if columns is None:
        all_columns = tuple(pf.columns + list(pf.cats))
    else:
        all_columns = columns
    if not isinstance(all_columns, tuple):
        out_type = Series
        all_columns = (all_columns,)
    else:
        out_type = DataFrame
    if index_col and index_col not in all_columns:
        all_columns = all_columns + (index_col,)

    dtypes = {k: ('category' if k in (categories or []) else v) for k, v in
              pf.dtypes.items() if k in all_columns}

    meta = pd.DataFrame({c: pd.Series([], dtype=d)
                        for (c, d) in dtypes.items()},
                        columns=[c for c in pf.columns if c in dtypes])

    for cat in categories:
        meta[cat] = pd.Series(pd.Categorical([], categories=cats[cat]))

    if index_col:
        meta = meta.set_index(index_col)

    if out_type == Series:
        assert len(meta.columns) == 1
        meta = meta[meta.columns[0]]

    dsk = {(name, i): (_read_parquet_row_group, myopen, pf.row_group_filename(rg),
                       index_col, all_columns, rg, out_type == Series,
                       categories, pf.helper, pf.cats, pf.dtypes)
           for i, rg in enumerate(rgs)}

    if index_col:
        divisions = list(minmax[index_col]['min']) + [minmax[index_col]['max'][-1]]
    else:
        divisions = (None,) * (len(rgs) + 1)

    return out_type(dsk, name, meta, divisions)
