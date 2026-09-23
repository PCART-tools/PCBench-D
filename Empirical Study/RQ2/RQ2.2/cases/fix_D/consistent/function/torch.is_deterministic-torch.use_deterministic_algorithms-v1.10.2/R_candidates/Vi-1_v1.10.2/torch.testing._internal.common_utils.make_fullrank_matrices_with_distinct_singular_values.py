def make_fullrank_matrices_with_distinct_singular_values(*shape, device, dtype):
    assert shape[-1] == shape[-2]
    t = make_tensor(shape, device=device, dtype=dtype)
    u, _, vh = torch.linalg.svd(t, full_matrices=False)
    # TODO: improve the handling of complex tensors here
    real_dtype = t.real.dtype if t.dtype.is_complex else t.dtype
    s = torch.arange(1., shape[-1] + 1, dtype=real_dtype, device=device).mul_(1.0 / (shape[-1] + 1))
    return (u * s.to(dtype)) @ vh
