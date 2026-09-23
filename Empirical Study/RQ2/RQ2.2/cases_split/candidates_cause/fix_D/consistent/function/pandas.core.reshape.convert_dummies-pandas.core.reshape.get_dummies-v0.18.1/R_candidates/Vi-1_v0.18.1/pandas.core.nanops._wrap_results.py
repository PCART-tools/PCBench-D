def _wrap_results(result, dtype):
    """ wrap our results if needed """

    if is_datetime64_dtype(dtype):
        if not isinstance(result, np.ndarray):
            result = lib.Timestamp(result)
        else:
            result = result.view(dtype)
    elif is_timedelta64_dtype(dtype):
        if not isinstance(result, np.ndarray):

            # raise if we have a timedelta64[ns] which is too large
            if np.fabs(result) > _int64_max:
                raise ValueError("overflow in timedelta operation")

            result = lib.Timedelta(result, unit='ns')
        else:
            result = result.astype('i8').view(dtype)

    return result
