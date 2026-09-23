def numpy_to_idxs(idxs: np.ndarray[Any, Any], size: int) -> pl.Series:
    # Unsigned or signed Numpy array (ordered from fastest to slowest).
    #   - np.uint32 (polars) or np.uint64 (polars_u64_idx) numpy array
    #     indexes.
    #   - Other unsigned numpy array indexes are converted to pl.UInt32
    #     (polars) or pl.UInt64 (polars_u64_idx).
    #   - Signed numpy array indexes are converted pl.UInt32 (polars) or
    #     pl.UInt64 (polars_u64_idx) after negative indexes are converted
    #     to absolute indexes.
    if idxs.ndim != 1:
        raise ValueError("only 1D numpy array is supported as index")

    idx_type = get_index_type()

    if len(idxs) == 0:
        return pl.Series("", [], dtype=idx_type)

    # Numpy array with signed or unsigned integers.
    if idxs.dtype.kind not in ("i", "u"):
        raise NotImplementedError("unsupported idxs datatype.")

    if idx_type == UInt32:
        if idxs.dtype in {np.int64, np.uint64} and idxs.max() >= 2**32:
            raise ValueError("index positions should be smaller than 2^32")
        if idxs.dtype == np.int64 and idxs.min() < -(2**32):
            raise ValueError("index positions should be bigger than -2^32 + 1")

    if idxs.dtype.kind == "i" and idxs.min() < 0:
        if idx_type == UInt32:
            if idxs.dtype in (np.int8, np.int16):
                idxs = idxs.astype(np.int32)
        else:
            if idxs.dtype in (np.int8, np.int16, np.int32):
                idxs = idxs.astype(np.int64)

        # Update negative indexes to absolute indexes.
        idxs = np.where(idxs < 0, size + idxs, idxs)

    # numpy conversion is much faster
    idxs = idxs.astype(np.uint32) if idx_type == UInt32 else idxs.astype(np.uint64)

    return pl.Series("", idxs, dtype=idx_type)
