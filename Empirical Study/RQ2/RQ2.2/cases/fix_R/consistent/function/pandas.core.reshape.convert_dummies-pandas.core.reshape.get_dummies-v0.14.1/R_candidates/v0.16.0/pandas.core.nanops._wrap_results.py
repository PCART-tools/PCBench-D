def _wrap_results(result, dtype):
    """ wrap our results if needed """

    if is_datetime64_dtype(dtype):
        if not isinstance(result, np.ndarray):
            result = lib.Timestamp(result)
        else:
            result = result.view(dtype)
    elif is_timedelta64_dtype(dtype):
        if not isinstance(result, np.ndarray):
            result = lib.Timedelta(result)
        else:
            result = result.astype('i8').view(dtype)

    return result
