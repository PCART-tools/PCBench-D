def _list_to_arrays(data, columns, coerce_float=False, dtype=None):
    if len(data) > 0 and isinstance(data[0], tuple):
        content = list(lib.to_object_array_tuples(data).T)
    else:
        # list of lists
        content = list(lib.to_object_array(data).T)
    return _convert_object_array(content, columns, dtype=dtype,
                                 coerce_float=coerce_float)
