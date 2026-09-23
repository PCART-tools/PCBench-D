def _has_infs(result):
    if isinstance(result, np.ndarray):
        if result.dtype == 'f8':
            return lib.has_infs_f8(result.ravel())
        elif result.dtype == 'f4':
            return lib.has_infs_f4(result.ravel())
    try:
        return np.isinf(result).any()
    except (TypeError, NotImplementedError) as e:
        # if it doesn't support infs, then it can't have infs
        return False
