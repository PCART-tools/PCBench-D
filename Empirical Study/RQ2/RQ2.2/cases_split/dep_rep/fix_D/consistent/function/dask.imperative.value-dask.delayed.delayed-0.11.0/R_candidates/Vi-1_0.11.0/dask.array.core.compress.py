@wraps(np.compress)
def compress(condition, a, axis=None):
    if axis is None:
        raise NotImplementedError("Must select axis for compression")
    if not -a.ndim <= axis < a.ndim:
        raise ValueError('axis=(%s) out of bounds' % axis)
    if axis < 0:
        axis += a.ndim

    condition = np.array(condition, dtype=bool)
    if condition.ndim != 1:
        raise ValueError("Condition must be one dimensional")
    if len(condition) < a.shape[axis]:
        condition = condition.copy()
        condition.resize(a.shape[axis])

    slc = ((slice(None),) * axis
         + (condition,)
         + (slice(None),) * (a.ndim - axis - 1))
    return a[slc]
