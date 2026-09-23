def _maybe_upcast_putmask(result, mask, other):
    """
    A safe version of putmask that potentially upcasts the result

    Parameters
    ----------
    result : ndarray
        The destination array. This will be mutated in-place if no upcasting is
        necessary.
    mask : boolean ndarray
    other : ndarray or scalar
        The source array or value

    Returns
    -------
    result : ndarray
    changed : boolean
        Set to true if the result array was upcasted
    """

    if mask.any():
        # Two conversions for date-like dtypes that can't be done automatically
        # in np.place:
        #   NaN -> NaT
        #   integer or integer array -> date-like array
        if result.dtype in _DATELIKE_DTYPES:
            if lib.isscalar(other):
                if isnull(other):
                    other = result.dtype.type('nat')
                elif is_integer(other):
                    other = np.array(other, dtype=result.dtype)
            elif is_integer_dtype(other):
                other = np.array(other, dtype=result.dtype)

        def changeit():

            # try to directly set by expanding our array to full
            # length of the boolean
            try:
                om = other[mask]
                om_at = om.astype(result.dtype)
                if (om == om_at).all():
                    new_result = result.values.copy()
                    new_result[mask] = om_at
                    result[:] = new_result
                    return result, False
            except:
                pass

            # we are forced to change the dtype of the result as the input
            # isn't compatible
            r, _ = _maybe_upcast(result, fill_value=other, copy=True)
            np.place(r, mask, other)

            return r, True

        # we want to decide whether place will work
        # if we have nans in the False portion of our mask then we need to
        # upcast (possibly), otherwise we DON't want to upcast (e.g. if we
        # have values, say integers, in the success portion then it's ok to not
        # upcast)
        new_dtype, _ = _maybe_promote(result.dtype, other)
        if new_dtype != result.dtype:

            # we have a scalar or len 0 ndarray
            # and its nan and we are changing some values
            if (lib.isscalar(other) or
                    (isinstance(other, np.ndarray) and other.ndim < 1)):
                if isnull(other):
                    return changeit()

            # we have an ndarray and the masking has nans in it
            else:

                if isnull(other[mask]).any():
                    return changeit()

        try:
            np.place(result, mask, other)
        except:
            return changeit()

    return result, False
