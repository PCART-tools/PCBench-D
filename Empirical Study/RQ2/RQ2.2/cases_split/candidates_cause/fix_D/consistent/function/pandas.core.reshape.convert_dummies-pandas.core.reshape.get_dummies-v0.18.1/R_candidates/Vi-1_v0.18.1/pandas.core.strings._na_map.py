def _na_map(f, arr, na_result=np.nan, dtype=object):
    # should really _check_ for NA
    return _map(f, arr, na_mask=True, na_value=na_result, dtype=dtype)
