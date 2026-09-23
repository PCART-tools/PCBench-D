def nanargmax(values, axis=None, skipna=True):
    """
    Returns -1 in the NA case
    """
    values, mask, dtype, _ = _get_values(values, skipna, fill_value_typ='-inf',
                                         isfinite=True)
    result = values.argmax(axis)
    result = _maybe_arg_null_out(result, axis, mask, skipna)
    return result
