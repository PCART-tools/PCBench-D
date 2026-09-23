def _to_arrays(data, columns, coerce_float=False, dtype=None):
    """
    Return list of arrays, columns
    """
    if isinstance(data, DataFrame):
        if columns is not None:
            arrays = [data.icol(i).values for i, col in enumerate(data.columns)
                      if col in columns]
        else:
            columns = data.columns
            arrays = [data.icol(i).values for i in range(len(columns))]

        return arrays, columns

    if not len(data):
        if isinstance(data, np.ndarray):
            columns = data.dtype.names
            if columns is not None:
                return [[]] * len(columns), columns
        return [], []  # columns if columns is not None else []
    if isinstance(data[0], (list, tuple)):
        return _list_to_arrays(data, columns, coerce_float=coerce_float,
                               dtype=dtype)
    elif isinstance(data[0], collections.Mapping):
        return _list_of_dict_to_arrays(data, columns,
                                       coerce_float=coerce_float,
                                       dtype=dtype)
    elif isinstance(data[0], Series):
        return _list_of_series_to_arrays(data, columns,
                                         coerce_float=coerce_float,
                                         dtype=dtype)
    elif isinstance(data[0], Categorical):
        if columns is None:
            columns = _default_index(len(data))
        return data, columns
    elif (isinstance(data, (np.ndarray, Series, Index))
          and data.dtype.names is not None):

        columns = list(data.dtype.names)
        arrays = [data[k] for k in columns]
        return arrays, columns
    else:
        # last ditch effort
        data = lmap(tuple, data)
        return _list_to_arrays(data, columns,
                               coerce_float=coerce_float,
                               dtype=dtype)
