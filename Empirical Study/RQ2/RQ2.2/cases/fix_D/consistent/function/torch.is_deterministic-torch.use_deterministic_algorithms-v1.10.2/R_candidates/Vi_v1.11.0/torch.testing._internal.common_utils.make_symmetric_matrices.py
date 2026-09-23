def make_symmetric_matrices(*shape, device, dtype):
    assert shape[-1] == shape[-2]
    t = make_tensor(shape, device=device, dtype=dtype)
    t = (t + t.mT).div_(2)
    return t
