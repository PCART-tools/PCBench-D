def unique(x, series_name=None):
    # unique returns np.ndarray, it must be wrapped
    return pd.Series(pd.Series.unique(x), name=series_name)
