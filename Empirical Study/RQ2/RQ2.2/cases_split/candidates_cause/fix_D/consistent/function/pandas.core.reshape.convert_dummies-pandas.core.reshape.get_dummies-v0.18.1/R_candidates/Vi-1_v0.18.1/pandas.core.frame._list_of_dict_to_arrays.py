def _list_of_dict_to_arrays(data, columns, coerce_float=False, dtype=None):
    if columns is None:
        gen = (list(x.keys()) for x in data)
        columns = lib.fast_unique_multiple_list_gen(gen)

    # assure that they are of the base dict class and not of derived
    # classes
    data = [(type(d) is dict) and d or dict(d) for d in data]

    content = list(lib.dicts_to_array(data, list(columns)).T)
    return _convert_object_array(content, columns, dtype=dtype,
                                 coerce_float=coerce_float)
