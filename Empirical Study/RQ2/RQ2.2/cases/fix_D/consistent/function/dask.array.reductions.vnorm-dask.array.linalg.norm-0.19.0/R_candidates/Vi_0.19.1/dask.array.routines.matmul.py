@wraps(np.matmul)
def matmul(a, b):
    a = asanyarray(a)
    b = asanyarray(b)

    if a.ndim == 0 or b.ndim == 0:
        raise ValueError("`matmul` does not support scalars.")

    a_is_1d = False
    if a.ndim == 1:
        a_is_1d = True
        a = a[np.newaxis, :]

    b_is_1d = False
    if b.ndim == 1:
        b_is_1d = True
        b = b[:, np.newaxis]

    if a.ndim < b.ndim:
        a = a[(b.ndim - a.ndim) * (np.newaxis,)]
    elif a.ndim > b.ndim:
        b = b[(a.ndim - b.ndim) * (np.newaxis,)]

    out = atop(
        np.matmul, tuple(range(1, a.ndim + 1)),
        a, tuple(range(1, a.ndim - 1)) + (a.ndim - 1, 0,),
        b, tuple(range(1, a.ndim - 1)) + (0, a.ndim,),
        dtype=result_type(a, b),
        concatenate=True
    )

    if a_is_1d:
        out = out[..., 0, :]
    if b_is_1d:
        out = out[..., 0]

    return out
