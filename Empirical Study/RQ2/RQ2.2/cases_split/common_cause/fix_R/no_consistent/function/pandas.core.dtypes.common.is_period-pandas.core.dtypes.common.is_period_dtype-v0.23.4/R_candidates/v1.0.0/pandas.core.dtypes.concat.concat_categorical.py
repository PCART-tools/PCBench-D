def concat_categorical(to_concat, axis: int = 0):
    """Concatenate an object/categorical array of arrays, each of which is a
    single dtype

    Parameters
    ----------
    to_concat : array of arrays
    axis : int
        Axis to provide concatenation in the current implementation this is
        always 0, e.g. we only have 1D categoricals

    Returns
    -------
    Categorical
        A single array, preserving the combined dtypes
    """

    # we could have object blocks and categoricals here
    # if we only have a single categoricals then combine everything
    # else its a non-compat categorical
    categoricals = [x for x in to_concat if is_categorical_dtype(x.dtype)]

    # validate the categories
    if len(categoricals) != len(to_concat):
        pass
    else:
        # when all categories are identical
        first = to_concat[0]
        if all(first.is_dtype_equal(other) for other in to_concat[1:]):
            return union_categoricals(categoricals)

    # extract the categoricals & coerce to object if needed
    to_concat = [
        x._internal_get_values()
        if is_categorical_dtype(x.dtype)
        else np.asarray(x).ravel()
        if not is_datetime64tz_dtype(x)
        else np.asarray(x.astype(object))
        for x in to_concat
    ]
    result = concat_compat(to_concat)
    if axis == 1:
        result = result.reshape(1, len(result))
    return result
