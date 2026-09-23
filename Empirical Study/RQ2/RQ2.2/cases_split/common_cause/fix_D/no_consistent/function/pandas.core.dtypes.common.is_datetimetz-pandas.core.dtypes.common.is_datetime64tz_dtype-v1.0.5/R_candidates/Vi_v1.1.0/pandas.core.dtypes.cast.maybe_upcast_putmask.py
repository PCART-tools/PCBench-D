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
    >>> arr = np.arange(1, 6)
    >>> mask = np.array([False, True, False, True, True])
    >>> result, _ = maybe_upcast_putmask(arr, mask, False)
    >>> result
    array([1, 0, 3, 0, 0])
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
            if isna(other):
                return changeit()

        try:
            np.place(result, mask, other)
        except TypeError:
            # e.g. int-dtype result and float-dtype other
            return changeit()

    return result, False
