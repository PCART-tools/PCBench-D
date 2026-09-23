def _maybe_upcast_putmask(result, mask, other, dtype=None, change=None):
    """ a safe version of put mask that (potentially upcasts the result
    return the result
    if change is not None, then MUTATE the change (and change the dtype)
    return a changed flag
    """

    if mask.any():

        other = _maybe_cast_scalar(result.dtype, other)

        def changeit():

            # try to directly set by expanding our array to full
            # length of the boolean
            try:
                om = other[mask]
                om_at = om.astype(result.dtype)
                if (om == om_at).all():
                    new_other = result.values.copy()
                    new_other[mask] = om_at
                    result[:] = new_other
                    return result, False
            except:
                pass

            # we are forced to change the dtype of the result as the input
            # isn't compatible
            r, fill_value = _maybe_upcast(
                result, fill_value=other, dtype=dtype, copy=True)
            np.putmask(r, mask, other)

            # we need to actually change the dtype here
            if change is not None:

                # if we are trying to do something unsafe
                # like put a bigger dtype in a smaller one, use the smaller one
                # pragma: no cover
                if change.dtype.itemsize < r.dtype.itemsize:
                    raise AssertionError(
                        "cannot change dtype of input to smaller size")
                change.dtype = r.dtype
                change[:] = r

            return r, True

        # we want to decide whether putmask will work
        # if we have nans in the False portion of our mask then we need to
        # upcast (possibily) otherwise we DON't want to upcast (e.g. if we are
        # have values, say integers in the success portion then its ok to not
        # upcast)
        new_dtype, fill_value = _maybe_promote(result.dtype, other)
        if new_dtype != result.dtype:

            # we have a scalar or len 0 ndarray
            # and its nan and we are changing some values
            if (np.isscalar(other) or
                    (isinstance(other, np.ndarray) and other.ndim < 1)):
                if isnull(other):
                    return changeit()

            # we have an ndarray and the masking has nans in it
            else:

                if isnull(other[mask]).any():
                    return changeit()

        try:
            np.putmask(result, mask, other)
        except:
            return changeit()

    return result, False
