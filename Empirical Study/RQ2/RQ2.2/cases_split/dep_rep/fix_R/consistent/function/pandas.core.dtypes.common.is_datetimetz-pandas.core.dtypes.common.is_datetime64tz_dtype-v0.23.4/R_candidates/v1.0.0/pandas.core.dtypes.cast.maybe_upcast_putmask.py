def maybe_upcast_putmask(result: np.ndarray, mask: np.ndarray, other):
    """
    A safe version of putmask that potentially upcasts the result.
    The result is replaced with the first N elements of other,
    where N is the number of True values in mask.
    If the length of other is shorter than N, other will be repeated.

    Parameters
    ----------
    result : ndarray
        The destination array. This will be mutated in-place if no upcasting is
        necessary.
    mask : boolean ndarray
    other : scalar
        The source value.

    Returns
    -------
    result : ndarray
    changed : bool
        Set to true if the result array was upcasted.

    Examples
    --------
    >>> result, _ = maybe_upcast_putmask(np.arange(1,6),
    np.array([False, True, False, True, True]), np.arange(21,23))
    >>> result
    array([1, 21, 3, 22, 21])
    """

    if not isinstance(result, np.ndarray):
        raise ValueError("The result input must be a ndarray.")
    if not is_scalar(other):
        # We _could_ support non-scalar other, but until we have a compelling
        #  use case, we assume away the possibility.
        raise ValueError("other must be a scalar")

    if mask.any():
        # Two conversions for date-like dtypes that can't be done automatically
        # in np.place:
        #   NaN -> NaT
        #   integer or integer array -> date-like array
        if result.dtype.kind in ["m", "M"]:
            if is_scalar(other):
                if isna(other):
                    other = result.dtype.type("nat")
                elif is_integer(other):
                    other = np.array(other, dtype=result.dtype)
            elif is_integer_dtype(other):
                other = np.array(other, dtype=result.dtype)

        def changeit():

            # try to directly set by expanding our array to full
            # length of the boolean
            try:
                om = other[mask]
            except (IndexError, TypeError):
                # IndexError occurs in test_upcast when we have a boolean
                #  mask of the wrong shape
                # TypeError occurs in test_upcast when `other` is a bool
                pass
            else:
                om_at = om.astype(result.dtype)
                if (om == om_at).all():
                    new_result = result.values.copy()
                    new_result[mask] = om_at
                    result[:] = new_result
                    return result, False

            # we are forced to change the dtype of the result as the input
            # isn't compatible
            r, _ = maybe_upcast(result, fill_value=other, copy=True)
            np.place(r, mask, other)

            return r, True

        # we want to decide whether place will work
        # if we have nans in the False portion of our mask then we need to
        # upcast (possibly), otherwise we DON't want to upcast (e.g. if we
        # have values, say integers, in the success portion then it's ok to not
        # upcast)
        new_dtype, _ = maybe_promote(result.dtype, other)
        if new_dtype != result.dtype:

            # we have a scalar or len 0 ndarray
            # and its nan and we are changing some values
            if is_scalar(other) or (isinstance(other, np.ndarray) and other.ndim < 1):
                if isna(other):
                    return changeit()

            # we have an ndarray and the masking has nans in it
            else:

                if isna(other).any():
                    return changeit()

        try:
            np.place(result, mask, other)
        except TypeError:
            # e.g. int-dtype result and float-dtype other
            return changeit()

    return result, False
