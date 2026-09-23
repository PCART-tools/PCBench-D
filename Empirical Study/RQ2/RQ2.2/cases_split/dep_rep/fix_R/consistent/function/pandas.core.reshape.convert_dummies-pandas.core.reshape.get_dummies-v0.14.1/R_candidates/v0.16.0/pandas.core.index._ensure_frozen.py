def _ensure_frozen(array_like, categories, copy=False):
    array_like = com._coerce_indexer_dtype(array_like, categories)
    array_like = array_like.view(FrozenNDArray)
    if copy:
        array_like = array_like.copy()
    return array_like
