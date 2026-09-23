def _putmask_smart(v, m, n):
    """
    Return a new block, try to preserve dtype if possible.

    Parameters
    ----------
    v : `values`, updated in-place (array like)
    m : `mask`, applies to both sides (array like)
    n : `new values` either scalar or an array like aligned with `values`
    """
    # n should be the length of the mask or a scalar here
    if not is_list_like(n):
        n = np.array([n] * len(m))
    elif isinstance(n, np.ndarray) and n.ndim == 0:  # numpy scalar
        n = np.repeat(np.array(n, ndmin=1), len(m))

    # see if we are only masking values that if putted
    # will work in the current dtype
    try:
        nn = n[m]

        # make sure that we have a nullable type
        # if we have nulls
        if not _is_na_compat(v, nn[0]):
            raise ValueError

        nn_at = nn.astype(v.dtype)

        # avoid invalid dtype comparisons
        if not is_numeric_v_string_like(nn, nn_at):
            comp = (nn == nn_at)
            if is_list_like(comp) and comp.all():
                nv = v.copy()
                nv[m] = nn_at
                return nv
    except (ValueError, IndexError, TypeError):
        pass

    # change the dtype
    dtype, _ = com._maybe_promote(n.dtype)
    nv = v.astype(dtype)
    try:
        nv[m] = n[m]
    except ValueError:
        idx, = np.where(np.squeeze(m))
        for mask_index, new_val in zip(idx, n[m]):
            nv[mask_index] = new_val
    return nv
