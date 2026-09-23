def concat_compat(to_concat, axis: AxisInt = 0, ea_compat_axis: bool = False):
    """
    provide concatenation of an array of arrays each of which is a single
    'normalized' dtypes (in that for example, if it's object, then it is a
    non-datetimelike and provide a combined dtype for the resulting array that
    preserves the overall dtype if possible)

    Parameters
    ----------
    to_concat : array of arrays
    axis : axis to provide concatenation
    ea_compat_axis : bool, default False
        For ExtensionArray compat, behave as if axis == 1 when determining
        whether to drop empty arrays.

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
    if non_empties and axis == 0 and not ea_compat_axis:
        # ea_compat_axis see GH#39574
        to_concat = non_empties

    dtypes = {obj.dtype for obj in to_concat}
    kinds = {obj.dtype.kind for obj in to_concat}
    contains_datetime = any(
        isinstance(dtype, (np.dtype, DatetimeTZDtype)) and dtype.kind in ["m", "M"]
        for dtype in dtypes
    ) or any(isinstance(obj, ABCExtensionArray) and obj.ndim > 1 for obj in to_concat)

    all_empty = not len(non_empties)
    single_dtype = len({x.dtype for x in to_concat}) == 1
    any_ea = any(isinstance(x.dtype, ExtensionDtype) for x in to_concat)

    if contains_datetime:
        return _concat_datetime(to_concat, axis=axis)

    if any_ea:
        # we ignore axis here, as internally concatting with EAs is always
        # for axis=0
        if not single_dtype:
            target_dtype = find_common_type([x.dtype for x in to_concat])
            target_dtype = common_dtype_categorical_compat(to_concat, target_dtype)
            to_concat = [
                astype_array(arr, target_dtype, copy=False) for arr in to_concat
            ]

        if isinstance(to_concat[0], ABCExtensionArray):
            # TODO: what about EA-backed Index?
            cls = type(to_concat[0])
            return cls._concat_same_type(to_concat)
        else:
            return np.concatenate(to_concat)

    elif all_empty:
        # we have all empties, but may need to coerce the result dtype to
        # object if we have non-numeric type operands (numpy would otherwise
        # cast this to float)
        if len(kinds) != 1:
            if not len(kinds - {"i", "u", "f"}) or not len(kinds - {"b", "i", "u"}):
                # let numpy coerce
                pass
            else:
                # coerce to object
                to_concat = [x.astype("object") for x in to_concat]
                kinds = {"o"}
    else:
        target_dtype = np_find_common_type(*dtypes)

    result = np.concatenate(to_concat, axis=axis)
    if "b" in kinds and result.dtype.kind in ["i", "u", "f"]:
        # GH#39817 cast to object instead of casting bools to numeric
        result = result.astype(object, copy=False)
    return result
