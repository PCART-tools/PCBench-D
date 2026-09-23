def _preprocess_slice_or_indexer(slice_or_indexer, length, allow_fill):
    if isinstance(slice_or_indexer, slice):
        return 'slice', slice_or_indexer, lib.slice_len(slice_or_indexer,
                                                        length)
    elif (isinstance(slice_or_indexer, np.ndarray) and
          slice_or_indexer.dtype == np.bool_):
        return 'mask', slice_or_indexer, slice_or_indexer.sum()
    else:
        indexer = np.asanyarray(slice_or_indexer, dtype=np.int64)
        if not allow_fill:
            indexer = maybe_convert_indices(indexer, length)
        return 'fancy', indexer, len(indexer)
