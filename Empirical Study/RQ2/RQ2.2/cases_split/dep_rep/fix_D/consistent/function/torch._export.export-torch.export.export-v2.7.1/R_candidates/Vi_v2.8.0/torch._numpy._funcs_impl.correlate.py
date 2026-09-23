def correlate(a: ArrayLike, v: ArrayLike, mode="valid"):
    v = torch.conj_physical(v)
    return _conv_corr_impl(a, v, mode)
