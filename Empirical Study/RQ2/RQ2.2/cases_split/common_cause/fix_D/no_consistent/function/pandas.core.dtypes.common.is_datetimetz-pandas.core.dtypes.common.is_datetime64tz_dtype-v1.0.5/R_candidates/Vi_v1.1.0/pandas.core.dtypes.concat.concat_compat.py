def concat_compat(to_concat, axis: int = 0):
    """
    provide concatenation of an array of arrays each of which is a single
    'normalized' dtypes (in that for example, if it's object, then it is a
    non-datetimelike and provide a combined dtype for the resulting array that
    preserves the overall dtype if possible)

    Parameters
    ----------
    to_concat : array of arrays
    axis : axis to provide concatenation

    Returns
    -------
    a single array, preserving the combined dtypes
    """
    # filter empty arrays
    # 1-d dtypes always are included here
    def is_nonempty(x) -> bool:
        if x.ndim <= axis:
            return True
        return x.shape[axis] > 0

    # If all arrays are empty, there's nothing to convert, just short-cut to
    # the concatenation, #3121.
    #
    # Creating an empty array directly is tempting, but the winnings would be
    # marginal given that it would still require shape & dtype calculation and
    # np.concatenate which has them both implemented is compiled.
    non_empties = [x for x in to_concat if is_nonempty(x)]
    if non_empties and axis == 0:
        to_concat = non_empties

    typs = get_dtype_kinds(to_concat)
    _contains_datetime = any(typ.startswith("datetime") for typ in typs)

    all_empty = not len(non_empties)
    single_dtype = len({x.dtype for x in to_concat}) == 1
    any_ea = any(is_extension_array_dtype(x.dtype) for x in to_concat)

    if any_ea:
        if not single_dtype:
            target_dtype = find_common_type([x.dtype for x in to_concat])
            to_concat = [_cast_to_common_type(arr, target_dtype) for arr in to_concat]

        if isinstance(to_concat[0], ExtensionArray) and axis == 0:
            cls = type(to_concat[0])
            return cls._concat_same_type(to_concat)
        else:
            return np.concatenate(to_concat, axis=axis)

    elif _contains_datetime or "timedelta" in typs:
        return concat_datetime(to_concat, axis=axis, typs=typs)

    elif all_empty:
        # we have all empties, but may need to coerce the result dtype to
        # object if we have non-numeric type operands (numpy would otherwise
        # cast this to float)
        typs = get_dtype_kinds(to_concat)
        if len(typs) != 1:

            if not len(typs - {"i", "u", "f"}) or not len(typs - {"bool", "i", "u"}):
                # let numpy coerce
                pass
            else:
                # coerce to object
                to_concat = [x.astype("object") for x in to_concat]

    return np.concatenate(to_concat, axis=axis)
