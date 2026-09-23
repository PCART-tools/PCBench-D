@wraps(np.tensordot)
def tensordot(lhs, rhs, axes=2):
    if isinstance(axes, Iterable):
        left_axes, right_axes = axes
    else:
        left_axes = tuple(range(lhs.ndim - 1, lhs.ndim - axes - 1, -1))
        right_axes = tuple(range(0, axes))

    if isinstance(left_axes, int):
        left_axes = (left_axes,)
    if isinstance(right_axes, int):
        right_axes = (right_axes,)
    if isinstance(left_axes, list):
        left_axes = tuple(left_axes)
    if isinstance(right_axes, list):
        right_axes = tuple(right_axes)

    if len(left_axes) > 1:
        raise NotImplementedError("Simultaneous Contractions of multiple "
                "indices not yet supported")

    if isinstance(lhs, np.ndarray):
        chunks = [(d,) for d in lhs.shape]
        chunks[left_axes[0]] = rhs.chunks[right_axes[0]]
        lhs = from_array(lhs, chunks=chunks)

    if isinstance(rhs, np.ndarray):
        chunks = [(d,) for d in rhs.shape]
        chunks[right_axes[0]] = lhs.chunks[left_axes[0]]
        rhs = from_array(rhs, chunks=chunks)

    if lhs._dtype is not None and rhs._dtype is not None :
        dt = np.promote_types(lhs._dtype, rhs._dtype)
    else:
        dt = None

    left_index = list(alphabet[:lhs.ndim])
    right_index = list(ALPHABET[:rhs.ndim])
    out_index = left_index + right_index

    for l, r in zip(left_axes, right_axes):
        out_index.remove(right_index[r])
        right_index[r] = left_index[l]

    func = partial(np.tensordot, axes=(left_axes, right_axes))
    intermediate = atop(func, out_index,
                        lhs, left_index,
                        rhs, right_index, dtype=dt)

    int_index = list(out_index)
    for l in left_axes:
        out_index.remove(left_index[l])

    return atop(sum, out_index, intermediate, int_index, dtype=dt)
