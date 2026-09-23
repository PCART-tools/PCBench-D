def dtype_for_core_type(core_type):
    for np_type, dt in _DATA_TYPE_FOR_DTYPE:
        if dt == core_type:
            return np_type
    raise TypeError('Unknown core type: ' + str(core_type))
