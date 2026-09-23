def _tensordot(a, b, axes):
    x = max([a, b], key=lambda x: x.__array_priority__)
    tensordot = tensordot_lookup.dispatch(type(x))

    # workaround may be removed when numpy version (currently 1.13.0) is bumped
    a_dims = np.array([a.shape[i] for i in axes[0]])
    b_dims = np.array([b.shape[i] for i in axes[1]])
    if len(a_dims) > 0 and (a_dims == b_dims).all() and a_dims.min() == 0:
        x = np.zeros(tuple([s for i, s in enumerate(a.shape) if i not in axes[0]] +
                           [s for i, s in enumerate(b.shape) if i not in axes[1]]))
    else:
        x = tensordot(a, b, axes=axes)

    ind = [slice(None, None)] * x.ndim
    for a in sorted(axes[0]):
        ind.insert(a, None)
    x = x[tuple(ind)]
    return x
