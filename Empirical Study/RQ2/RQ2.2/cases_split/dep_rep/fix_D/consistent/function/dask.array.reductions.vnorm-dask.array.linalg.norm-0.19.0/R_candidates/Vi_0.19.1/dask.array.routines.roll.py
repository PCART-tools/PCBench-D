@wraps(np.roll)
def roll(array, shift, axis=None):
    result = array

    if axis is None:
        result = ravel(result)

        if not isinstance(shift, Integral):
            raise TypeError(
                "Expect `shift` to be an instance of Integral"
                " when `axis` is None."
            )

        shift = (shift,)
        axis = (0,)
    else:
        try:
            len(shift)
        except TypeError:
            shift = (shift,)
        try:
            len(axis)
        except TypeError:
            axis = (axis,)

    if len(shift) != len(axis):
        raise ValueError("Must have the same number of shifts as axes.")

    for i, s in zip(axis, shift):
        s = -s
        s %= result.shape[i]

        sl1 = result.ndim * [slice(None)]
        sl2 = result.ndim * [slice(None)]

        sl1[i] = slice(s, None)
        sl2[i] = slice(None, s)

        sl1 = tuple(sl1)
        sl2 = tuple(sl2)

        result = concatenate([result[sl1], result[sl2]], axis=i)

    result = result.reshape(array.shape)

    return result
