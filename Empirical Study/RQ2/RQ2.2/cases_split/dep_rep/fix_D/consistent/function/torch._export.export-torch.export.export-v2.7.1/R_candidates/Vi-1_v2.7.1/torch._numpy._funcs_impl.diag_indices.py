def diag_indices(n, ndim=2):
    idx = torch.arange(n)
    return (idx,) * ndim
