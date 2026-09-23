def _maybe_null_out(result, axis, mask):
    if axis is not None and getattr(result, 'ndim', False):
        null_mask = (mask.shape[axis] - mask.sum(axis)) == 0
        if np.any(null_mask):
            if np.iscomplexobj(result):
                result = result.astype('c16')
            else:
                result = result.astype('f8')
            result[null_mask] = np.nan
    elif result is not tslib.NaT:
        null_mask = mask.size - mask.sum()
        if null_mask == 0:
            result = np.nan

    return result
