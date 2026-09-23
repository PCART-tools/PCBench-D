def coerce_dtypes(df, dtypes):
    """ Coerce dataframe to dtypes safely

    Operates in place

    Parameters
    ----------
    df: Pandas DataFrame
    dtypes: dict like {'x': float}
    """
    for c in df.columns:
        if c in dtypes and df.dtypes[c] != dtypes[c]:
            if (np.issubdtype(df.dtypes[c], np.floating) and
                    np.issubdtype(dtypes[c], np.integer)):
                if (df[c] % 1).any():
                    msg = ("Runtime type mismatch. "
                           "Add {'%s': float} to dtype= keyword in "
                           "read_csv/read_table")
                    raise TypeError(msg % c)
            df[c] = df[c].astype(dtypes[c])
