def _hashtable_algo(f, dtype, return_dtype=None):
    """
    f(HashTable, type_caster) -> result
    """
    if is_float_dtype(dtype):
        return f(htable.Float64HashTable, _ensure_float64)
    elif is_integer_dtype(dtype):
        return f(htable.Int64HashTable, _ensure_int64)
    elif is_datetime64_dtype(dtype):
        return_dtype = return_dtype or 'M8[ns]'
        return f(htable.Int64HashTable, _ensure_int64).view(return_dtype)
    elif is_timedelta64_dtype(dtype):
        return_dtype = return_dtype or 'm8[ns]'
        return f(htable.Int64HashTable, _ensure_int64).view(return_dtype)
    else:
        return f(htable.PyObjectHashTable, _ensure_object)
