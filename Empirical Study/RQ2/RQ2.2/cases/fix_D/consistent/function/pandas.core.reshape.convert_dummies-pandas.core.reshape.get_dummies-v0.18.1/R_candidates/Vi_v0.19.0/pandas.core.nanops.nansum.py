@disallow('M8')
@bottleneck_switch(zero_value=0)
def nansum(values, axis=None, skipna=True):
    values, mask, dtype, dtype_max = _get_values(values, skipna, 0)
    dtype_sum = dtype_max
    if is_float_dtype(dtype):
        dtype_sum = dtype
    elif is_timedelta64_dtype(dtype):
        dtype_sum = np.float64
    the_sum = values.sum(axis, dtype=dtype_sum)
    the_sum = _maybe_null_out(the_sum, axis, mask)

    return _wrap_results(the_sum, dtype)
