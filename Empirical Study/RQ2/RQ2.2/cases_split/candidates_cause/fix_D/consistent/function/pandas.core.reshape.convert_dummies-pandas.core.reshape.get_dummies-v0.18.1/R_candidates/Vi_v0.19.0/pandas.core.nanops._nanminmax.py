def _nanminmax(meth, fill_value_typ):
    @bottleneck_switch()
    def reduction(values, axis=None, skipna=True):
        values, mask, dtype, dtype_max = _get_values(
            values, skipna, fill_value_typ=fill_value_typ, )

        if ((axis is not None and values.shape[axis] == 0) or
                values.size == 0):
            try:
                result = getattr(values, meth)(axis, dtype=dtype_max)
                result.fill(np.nan)
            except:
                result = np.nan
        else:
            result = getattr(values, meth)(axis)

        result = _wrap_results(result, dtype)
        return _maybe_null_out(result, axis, mask)

    reduction.__name__ = 'nan' + meth
    return reduction
