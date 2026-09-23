@disallow('M8')
@bottleneck_switch()
def nanmedian(values, axis=None, skipna=True):

    values, mask, dtype, dtype_max = _get_values(values, skipna)

    def get_median(x):
        mask = notnull(x)
        if not skipna and not mask.all():
            return np.nan
        return algos.median(_values_from_object(x[mask]))

    if not is_float_dtype(values):
        values = values.astype('f8')
        values[mask] = np.nan

    if axis is None:
        values = values.ravel()

    notempty = values.size

    # an array from a frame
    if values.ndim > 1:
        # there's a non-empty array to apply over otherwise numpy raises
        if notempty:
            return _wrap_results(
                np.apply_along_axis(get_median, axis, values), dtype)

        # must return the correct shape, but median is not defined for the
        # empty set so return nans of shape "everything but the passed axis"
        # since "axis" is where the reduction would occur if we had a nonempty
        # array
        shp = np.array(values.shape)
        dims = np.arange(values.ndim)
        ret = np.empty(shp[dims != axis])
        ret.fill(np.nan)
        return _wrap_results(ret, dtype)

    # otherwise return a scalar value
    return _wrap_results(get_median(values) if notempty else np.nan, dtype)
