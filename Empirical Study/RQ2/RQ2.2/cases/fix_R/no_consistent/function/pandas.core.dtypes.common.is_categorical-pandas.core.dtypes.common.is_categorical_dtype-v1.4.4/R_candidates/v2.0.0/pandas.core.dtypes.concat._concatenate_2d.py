def _concatenate_2d(to_concat, axis: AxisInt):
    # coerce to 2d if needed & concatenate
    if axis == 1:
        to_concat = [np.atleast_2d(x) for x in to_concat]
    return np.concatenate(to_concat, axis=axis)
