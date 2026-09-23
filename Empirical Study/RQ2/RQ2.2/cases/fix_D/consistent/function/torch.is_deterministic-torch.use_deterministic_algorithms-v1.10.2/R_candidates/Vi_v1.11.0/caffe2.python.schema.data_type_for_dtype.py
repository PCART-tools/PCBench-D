def data_type_for_dtype(dtype):
    for np_type, dt in _DATA_TYPE_FOR_DTYPE:
        if dtype.base == np_type:
            return dt
    raise TypeError('Unknown dtype: ' + str(dtype.base))
