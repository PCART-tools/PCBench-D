def _try_loc(df, ind):
    try:
        return df.loc[ind]
    except KeyError:
        return df.head(0)
