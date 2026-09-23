def _safe_reshape(arr, new_shape):
    """
    If possible, reshape `arr` to have shape `new_shape`,
    with a couple of exceptions (see gh-13012):

    1) If `arr` is a Categorical or Index, `arr` will be
       returned as is.
    2) If `arr` is a Series, the `_values` attribute will
       be reshaped and returned.

    Parameters
    ----------
    arr : array-like, object to be reshaped
    new_shape : int or tuple of ints, the new shape
    """
    if isinstance(arr, ABCSeries):
        arr = arr._values
    if not isinstance(arr, Categorical):
        arr = arr.reshape(new_shape)
    return arr
