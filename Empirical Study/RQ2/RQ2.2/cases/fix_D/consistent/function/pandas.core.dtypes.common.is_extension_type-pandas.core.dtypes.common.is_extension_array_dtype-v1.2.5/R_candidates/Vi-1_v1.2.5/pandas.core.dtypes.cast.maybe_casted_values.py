def maybe_casted_values(
    index: "Index", codes: Optional[np.ndarray] = None
) -> ArrayLike:
    """
    Convert an index, given directly or as a pair (level, code), to a 1D array.

    Parameters
    ----------
    index : Index
    codes : np.ndarray[intp] or None, default None

    Returns
    -------
    ExtensionArray or ndarray
        If codes is `None`, the values of `index`.
        If codes is passed, an array obtained by taking from `index` the indices
        contained in `codes`.
    """

    values = index._values
    if values.dtype == np.object_:
        values = lib.maybe_convert_objects(values)

    # if we have the codes, extract the values with a mask
    if codes is not None:
        mask: np.ndarray = codes == -1

        if mask.size > 0 and mask.all():
            # we can have situations where the whole mask is -1,
            # meaning there is nothing found in codes, so make all nan's

            dtype = index.dtype
            fill_value = na_value_for_dtype(dtype)
            values = construct_1d_arraylike_from_scalar(fill_value, len(mask), dtype)

        else:
            values = values.take(codes)

            if mask.any():
                if isinstance(values, np.ndarray):
                    values, _ = maybe_upcast_putmask(values, mask, np.nan)
                else:
                    values[mask] = np.nan

    return values
