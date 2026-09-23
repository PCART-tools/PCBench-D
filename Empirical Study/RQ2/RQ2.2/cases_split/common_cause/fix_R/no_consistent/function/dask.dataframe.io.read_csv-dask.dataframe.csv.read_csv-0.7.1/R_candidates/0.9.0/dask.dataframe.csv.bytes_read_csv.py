def bytes_read_csv(b, header, kwargs, dtypes=None, columns=None):
    """ Convert a block of bytes to a Pandas DataFrame

    Parameters
    ----------
    b: bytestring
        The content to be parsed with pandas.read_csv
    header: bytestring
        An optional header to prepend to b
    kwargs: dict
        A dictionary of keyword arguments to be passed to pandas.read_csv
    dtypes: dict
        DTypes to assign to columns

    See Also:
        dask.dataframe.csv.read_csv_from_bytes
    """
    bio = BytesIO()
    if not b.startswith(header.rstrip()):
        bio.write(header)
    bio.write(b)
    bio.seek(0)
    df = pd.read_csv(bio, **kwargs)
    if dtypes:
        coerce_dtypes(df, dtypes)

    if columns and (list(df.columns) != list(columns)):
        raise ValueError("Columns do not match", df.columns, columns)
    return df
