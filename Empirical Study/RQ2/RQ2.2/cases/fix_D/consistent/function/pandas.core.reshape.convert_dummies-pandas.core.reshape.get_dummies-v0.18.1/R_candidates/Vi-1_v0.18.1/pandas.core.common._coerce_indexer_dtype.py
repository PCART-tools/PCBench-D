def _coerce_indexer_dtype(indexer, categories):
    """ coerce the indexer input array to the smallest dtype possible """
    l = len(categories)
    if l < _int8_max:
        return _ensure_int8(indexer)
    elif l < _int16_max:
        return _ensure_int16(indexer)
    elif l < _int32_max:
        return _ensure_int32(indexer)
    return _ensure_int64(indexer)
