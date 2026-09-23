def make_symmetric_pd_matrices(*shape, device, dtype):
    assert shape[-1] == shape[-2]
    t = make_tensor(shape, device=device, dtype=dtype)
    i = torch.eye(shape[-1], device=device, dtype=dtype) * 1e-5
    return t @ t.mT + i
