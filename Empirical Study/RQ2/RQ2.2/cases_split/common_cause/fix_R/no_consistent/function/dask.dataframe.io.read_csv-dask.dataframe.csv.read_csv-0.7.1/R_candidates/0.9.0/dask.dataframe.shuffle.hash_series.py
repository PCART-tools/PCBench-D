def hash_series(s):
    """Given a series, return a numpy array of deterministic integers."""
    vals = s.values
    dt = vals.dtype
    if is_categorical_dtype(dt):
        return vals.codes
    elif np.issubdtype(dt, np.integer):
        return vals
    elif np.issubdtype(dt, np.floating):
        return np.nan_to_num(vals).astype('int64')
    elif dt == np.bool:
        return vals.view('int8')
    elif np.issubdtype(dt, np.datetime64) or np.issubdtype(dt, np.timedelta64):
        return vals.view('int64')
    else:
        return s.apply(hash).values
