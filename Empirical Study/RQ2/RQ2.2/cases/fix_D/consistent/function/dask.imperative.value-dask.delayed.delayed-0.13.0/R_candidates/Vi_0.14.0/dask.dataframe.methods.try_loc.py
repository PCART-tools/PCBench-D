def try_loc(df, iindexer, cindexer=None):
    """
    .loc for unknown divisions
    """
    try:
        return loc(df, iindexer, cindexer)
    except KeyError:
        return df.head(0).loc[:, cindexer]
