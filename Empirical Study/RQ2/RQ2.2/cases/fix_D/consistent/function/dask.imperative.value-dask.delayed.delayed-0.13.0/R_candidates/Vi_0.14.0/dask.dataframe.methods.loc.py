def loc(df, iindexer, cindexer=None):
    """
    .loc for known divisions
    """
    if cindexer is None:
        return df.loc[iindexer]
    else:
        return df.loc[iindexer, cindexer]
