def random_fullrank_matrix_distinct_singular_value(matrix_size, *batch_dims,
                                                   **kwargs):
    dtype = kwargs.get('dtype', torch.double)
    device = kwargs.get('device', 'cpu')
    silent = kwargs.get("silent", False)
    if silent and not torch._C.has_lapack:
        return torch.ones(matrix_size, matrix_size, dtype=dtype, device=device)

    A = torch.randn(batch_dims + (matrix_size, matrix_size), dtype=dtype, device=device)
    u, _, vh = torch.linalg.svd(A, full_matrices=False)
    real_dtype = A.real.dtype if A.dtype.is_complex else A.dtype
    s = torch.arange(1., matrix_size + 1, dtype=real_dtype, device=device).mul_(1.0 / (matrix_size + 1))
    return (u * s.to(A.dtype)) @ vh
