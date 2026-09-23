def to_parquet(path, df, compression=None, write_index=None, has_nulls=None,
               fixed_text=None, object_encoding=None, storage_options=None,
               append=False, ignore_divisions=False):
    """
    Store Dask.dataframe to Parquet files

    Notes
    -----
    Each partition will be written to a separate file.

    Parameters
    ----------
    path : string
        Destination directory for data.  Prepend with protocol like ``s3://``
        or ``hdfs://`` for remote data.
    df : Dask.dataframe
    compression : string or dict
        Either a string like "SNAPPY" or a dictionary mapping column names to
        compressors like ``{"name": "GZIP", "values": "SNAPPY"}``
    write_index : boolean
        Whether or not to write the index.  Defaults to True *if* divisions are
        known.
    has_nulls : bool, list or None
        Specifies whether to write NULLs information for columns. If bools,
        apply to all columns, if list, use for only the named columns, if None,
        use only for columns which don't have a sentinel NULL marker (currently
        object columns only).
    fixed_text : dict {col: int}
        For column types that are written as bytes (bytes, utf8 strings, or
        json and bson-encoded objects), if a column is included here, the
        data will be written in fixed-length format, which should be faster
        but can potentially result in truncation.
    object_encoding : dict {col: bytes|utf8|json|bson} or str
        For object columns, specify how to encode to bytes. If a str, same
        encoding is applied to all object columns.
    storage_options : dict
        Key/value pairs to be passed on to the file-system backend, if any.
    append: bool (False)
        If False, construct data-set from scratch; if True, add new row-group(s)
        to existing data-set. In the latter case, the data-set must exist,
        and the schema must match the input data.
    ignore_divisions: bool (False)
        If False raises error when previous divisions overlap with the new
        appended divisions. Ignored if append=False.

    This uses the fastparquet project: http://fastparquet.readthedocs.io/en/latest

    Examples
    --------
    >>> df = dd.read_csv(...)  # doctest: +SKIP
    >>> to_parquet('/path/to/output/', df, compression='SNAPPY')  # doctest: +SKIP

    See Also
    --------
    read_parquet: Read parquet data to dask.dataframe
    """
    if fastparquet is False:
        raise ImportError("fastparquet not installed")

    myopen = OpenFileCreator(path, compression=None, text=False,
                             **(storage_options or {}))
    myopen.fs.mkdirs(path)
    sep = myopen.fs.sep
    metadata_fn = sep.join([path, '_metadata'])

    if write_index is True or write_index is None and df.known_divisions:
        new_divisions = df.divisions
        df = df.reset_index()
        index_col = df.columns[0]
    else:
        ignore_divisions = True

    object_encoding = object_encoding or 'utf8'
    if object_encoding == 'infer' or (isinstance(object_encoding, dict) and
                                      'infer' in object_encoding.values()):
        raise ValueError('"infer" not allowed as object encoding, '
                         'because this required data in memory.')
    fmd = fastparquet.writer.make_metadata(df._meta, has_nulls=has_nulls,
                                           fixed_text=fixed_text,
                                           object_encoding=object_encoding)

    if append:
        pf = fastparquet.api.ParquetFile(path, open_with=myopen)
        if pf.file_scheme != 'hive':
            raise ValueError('Requested file scheme is hive, '
                             'but existing file scheme is not.')
        elif set(pf.columns) != set(df.columns):
            raise ValueError('Appended columns not the same.\n'
                             'New: {} | Previous: {}'
                             .format(pf.columns, list(df.columns)))
        elif set(pf.dtypes.items()) != set(df.dtypes.items()):
            raise ValueError('Appended dtypes differ.\n{}'
                             .format(set(pf.dtypes.items()) ^
                                     set(df.dtypes.items())))
        # elif fmd.schema != pf.fmd.schema:
        #    raise ValueError('Appended schema differs.')
        else:
            df = df[pf.columns]

        fmd = pf.fmd
        i_offset = fastparquet.writer.find_max_part(fmd.row_groups)

        if not ignore_divisions:
            minmax = fastparquet.api.sorted_partitioned_columns(pf)
            divisions = list(minmax[index_col]['min']) + [
                minmax[index_col]['max'][-1]]

            if new_divisions[0] < divisions[-1]:
                raise ValueError(
                    'Appended divisions overlapping with the previous ones.\n'
                    'New: {} | Previous: {}'
                    .format(divisions[-1], new_divisions[0]))
    else:
        i_offset = 0

    partitions = df.to_delayed()
    filenames = ['part.%i.parquet' % i
                 for i in range(i_offset, len(partitions) + i_offset)]
    outfiles = [sep.join([path, fn]) for fn in filenames]

    writes = [delayed(fastparquet.writer.make_part_file)(
              myopen(outfile, 'wb'), partition, fmd.schema,
              compression=compression)
              for outfile, partition in zip(outfiles, partitions)]

    out = delayed(writes).compute()

    for fn, rg in zip(filenames, out):
        for chunk in rg.columns:
            chunk.file_path = fn
        fmd.row_groups.append(rg)

    fastparquet.writer.write_common_metadata(metadata_fn, fmd, open_with=myopen,
                                             no_row_groups=False)

    fn = sep.join([path, '_common_metadata'])
    fastparquet.writer.write_common_metadata(fn, fmd, open_with=myopen)
