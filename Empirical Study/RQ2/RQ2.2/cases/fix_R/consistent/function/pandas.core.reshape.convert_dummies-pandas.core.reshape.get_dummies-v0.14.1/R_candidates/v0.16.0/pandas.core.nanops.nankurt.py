@disallow('M8','m8')
def nankurt(values, axis=None, skipna=True):

    mask = isnull(values)
    if not is_floating_dtype(values):
        values = values.astype('f8')

    count = _get_counts(mask, axis)

    if skipna:
        values = values.copy()
        np.putmask(values, mask, 0)

    A = values.sum(axis) / count
    B = (values ** 2).sum(axis) / count - A ** 2
    C = (values ** 3).sum(axis) / count - A ** 3 - 3 * A * B
    D = (values ** 4).sum(axis) / count - A ** 4 - 6 * B * A * A - 4 * C * A

    B = _zero_out_fperr(B)
    D = _zero_out_fperr(D)

    if not isinstance(B, np.ndarray):
        # if B is a scalar, check these corner cases first before doing division
        if count < 4:
            return np.nan
        if B == 0:
            return 0

    result = (((count * count - 1.) * D / (B * B) - 3 * ((count - 1.) ** 2)) /
              ((count - 2.) * (count - 3.)))

    if isinstance(result, np.ndarray):
        result = np.where(B == 0, 0, result)
        result[count < 4] = np.nan

    return result
