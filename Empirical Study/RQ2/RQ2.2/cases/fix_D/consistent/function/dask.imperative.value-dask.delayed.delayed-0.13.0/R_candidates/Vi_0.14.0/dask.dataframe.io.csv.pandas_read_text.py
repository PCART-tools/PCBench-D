def pandas_read_text(reader, b, header, kwargs, dtypes=None, columns=None,
                     write_header=True, enforce=False):
    """ Convert a block of bytes to a Pandas DataFrame

    Parameters
    ----------
    reader : callable
        ``pd.read_csv`` or ``pd.read_table``.
    b : bytestring
        The content to be parsed with ``reader``
    header : bytestring
        An optional header to prepend to ``b``
    kwargs : dict
        A dictionary of keyword arguments to be passed to ``reader``
    dtypes : dict
        DTypes to assign to columns

    See Also
    --------
    dask.dataframe.csv.read_pandas_from_bytes
    """
    bio = BytesIO()
    if write_header and not b.startswith(header.rstrip()):
        bio.write(header)
    bio.write(b)
    bio.seek(0)
    df = reader(bio, **kwargs)
    if dtypes:
        coerce_dtypes(df, dtypes)

    if enforce and columns and (list(df.columns) != list(columns)):
        raise ValueError("Columns do not match", df.columns, columns)
    elif columns:
        df.columns = columns
    return df
