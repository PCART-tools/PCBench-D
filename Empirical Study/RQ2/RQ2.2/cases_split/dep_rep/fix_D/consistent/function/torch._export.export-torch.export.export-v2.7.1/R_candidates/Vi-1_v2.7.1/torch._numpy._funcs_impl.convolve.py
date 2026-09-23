def convolve(a: ArrayLike, v: ArrayLike, mode="full"):
    # NumPy: if v is longer than a, the arrays are swapped before computation
    if a.shape[0] < v.shape[0]:
        a, v = v, a

    # flip the weights since numpy does and torch does not
    v = torch.flip(v, (0,))

    return _conv_corr_impl(a, v, mode)
