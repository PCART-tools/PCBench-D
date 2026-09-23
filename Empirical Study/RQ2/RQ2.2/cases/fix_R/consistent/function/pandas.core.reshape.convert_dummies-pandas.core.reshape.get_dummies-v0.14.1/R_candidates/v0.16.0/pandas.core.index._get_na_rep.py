def _get_na_rep(dtype):
    return {np.datetime64: 'NaT', np.timedelta64: 'NaT'}.get(dtype, 'NaN')
