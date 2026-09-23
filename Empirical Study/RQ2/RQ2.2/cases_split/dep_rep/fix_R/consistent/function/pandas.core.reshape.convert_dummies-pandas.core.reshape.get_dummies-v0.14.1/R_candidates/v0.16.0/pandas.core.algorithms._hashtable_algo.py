def _hashtable_algo(f, dtype):
    """
    f(HashTable, type_caster) -> result
    """
    if com.is_float_dtype(dtype):
        return f(htable.Float64HashTable, com._ensure_float64)
    elif com.is_integer_dtype(dtype):
        return f(htable.Int64HashTable, com._ensure_int64)
    else:
        return f(htable.PyObjectHashTable, com._ensure_object)
