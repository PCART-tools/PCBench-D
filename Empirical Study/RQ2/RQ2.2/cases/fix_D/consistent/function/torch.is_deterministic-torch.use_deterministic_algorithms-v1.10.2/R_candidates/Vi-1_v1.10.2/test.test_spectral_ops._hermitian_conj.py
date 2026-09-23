def _hermitian_conj(x, dim):
    """Returns the hermitian conjugate along a single dimension

    H(x)[i] = conj(x[-i])
    """
    out = torch.empty_like(x)
    mid = (x.size(dim) - 1) // 2
    idx = [slice(None)] * out.dim()
    idx_center = list(idx)
    idx_center[dim] = 0
    out[idx] = x[idx]

    idx_neg = list(idx)
    idx_neg[dim] = slice(-mid, None)
    idx_pos = idx
    idx_pos[dim] = slice(1, mid + 1)

    out[idx_pos] = x[idx_neg].flip(dim)
    out[idx_neg] = x[idx_pos].flip(dim)
    if (2 * mid + 1 < x.size(dim)):
        idx[dim] = mid + 1
        out[idx] = x[idx]
    return out.conj()
