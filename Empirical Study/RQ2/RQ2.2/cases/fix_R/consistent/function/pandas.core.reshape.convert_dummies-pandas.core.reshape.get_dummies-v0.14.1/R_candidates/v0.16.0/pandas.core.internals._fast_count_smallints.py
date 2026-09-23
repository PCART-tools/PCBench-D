def _fast_count_smallints(arr):
    """Faster version of set(arr) for sequences of small numbers."""
    if len(arr) == 0:
        # Handle empty arr case separately: numpy 1.6 chokes on that.
        return np.empty((0, 2), dtype=arr.dtype)
    else:
        counts = np.bincount(arr.astype(np.int_))
        nz = counts.nonzero()[0]
        return np.c_[nz, counts[nz]]
