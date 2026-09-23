def _get_na_value(dtype):
    return {np.datetime64: tslib.NaT, np.timedelta64: tslib.NaT}.get(dtype,
                                                                     np.nan)
