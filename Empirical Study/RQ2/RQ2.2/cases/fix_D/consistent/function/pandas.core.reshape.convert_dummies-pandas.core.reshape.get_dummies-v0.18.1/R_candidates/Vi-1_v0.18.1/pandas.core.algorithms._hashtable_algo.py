def _hashtable_algo(f, dtype, return_dtype=None):
    """
    f(HashTable, type_caster) -> result
    """
    if com.is_float_dtype(dtype):
        return f(htable.Float64HashTable, com._ensure_float64)
    elif com.is_integer_dtype(dtype):
        return f(htable.Int64HashTable, com._ensure_int64)
    elif com.is_datetime64_dtype(dtype):
        return_dtype = return_dtype or 'M8[ns]'
        return f(htable.Int64HashTable, com._ensure_int64).view(return_dtype)
    elif com.is_timedelta64_dtype(dtype):
        return_dtype = return_dtype or 'm8[ns]'
        return f(htable.Int64HashTable, com._ensure_int64).view(return_dtype)
    else:
        return f(htable.PyObjectHashTable, com._ensure_object)
