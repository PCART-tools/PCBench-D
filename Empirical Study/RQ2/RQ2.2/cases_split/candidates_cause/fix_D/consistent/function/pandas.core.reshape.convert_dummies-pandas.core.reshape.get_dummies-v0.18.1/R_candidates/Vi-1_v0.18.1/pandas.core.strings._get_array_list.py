def _get_array_list(arr, others):
    from pandas.core.series import Series

    if len(others) and isinstance(_values_from_object(others)[0],
                                  (list, np.ndarray, Series)):
        arrays = [arr] + list(others)
    else:
        arrays = [arr, others]

    return [np.asarray(x, dtype=object) for x in arrays]
