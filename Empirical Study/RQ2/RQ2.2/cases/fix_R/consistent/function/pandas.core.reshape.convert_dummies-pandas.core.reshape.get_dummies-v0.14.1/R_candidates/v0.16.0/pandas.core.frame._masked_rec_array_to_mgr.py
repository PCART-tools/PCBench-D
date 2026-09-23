def _masked_rec_array_to_mgr(data, index, columns, dtype, copy):
    """ extract from a masked rec array and create the manager """

    # essentially process a record array then fill it
    fill_value = data.fill_value
    fdata = ma.getdata(data)
    if index is None:
        index = _get_names_from_index(fdata)
        if index is None:
            index = _default_index(len(data))
    index = _ensure_index(index)

    if columns is not None:
        columns = _ensure_index(columns)
    arrays, arr_columns = _to_arrays(fdata, columns)

    # fill if needed
    new_arrays = []
    for fv, arr, col in zip(fill_value, arrays, arr_columns):
        mask = ma.getmaskarray(data[col])
        if mask.any():
            arr, fv = _maybe_upcast(arr, fill_value=fv, copy=True)
            arr[mask] = fv
        new_arrays.append(arr)

    # create the manager
    arrays, arr_columns = _reorder_arrays(new_arrays, arr_columns, columns)
    if columns is None:
        columns = arr_columns

    mgr = _arrays_to_mgr(arrays, arr_columns, index, columns)

    if copy:
        mgr = mgr.copy()
    return mgr
