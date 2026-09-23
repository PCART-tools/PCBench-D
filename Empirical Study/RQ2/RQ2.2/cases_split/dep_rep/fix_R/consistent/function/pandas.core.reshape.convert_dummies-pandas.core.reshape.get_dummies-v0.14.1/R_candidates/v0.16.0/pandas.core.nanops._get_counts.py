def _get_counts(mask, axis):
    if axis is None:
        return float(mask.size - mask.sum())

    count = mask.shape[axis] - mask.sum(axis)
    try:
        return count.astype(float)
    except AttributeError:
        return np.array(count, dtype=float)
