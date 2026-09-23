def wrapped_pad_func(array, pad_func, iaxis_pad_width, iaxis, pad_func_kwargs):
    result = array.copy()
    for i in np.ndindex(array.shape[:iaxis] + array.shape[iaxis + 1:]):
        i = i[:iaxis] + (slice(None),) + i[iaxis:]
        result[i] = pad_func(array[i], iaxis_pad_width, iaxis, pad_func_kwargs)

    return result
