def unique(x, series_name=None):
    # unique returns np.ndarray, it must be wrapped
    return pd.Series(x.unique(), name=series_name)
