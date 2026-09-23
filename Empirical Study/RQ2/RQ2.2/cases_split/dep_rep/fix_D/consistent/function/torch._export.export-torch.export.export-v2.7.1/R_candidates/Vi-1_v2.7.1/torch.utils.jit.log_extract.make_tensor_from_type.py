def make_tensor_from_type(inp_type: torch._C.TensorType):
    size = inp_type.sizes()
    stride = inp_type.strides()
    device = inp_type.device()
    dtype = inp_type.dtype()
    assert size is not None
    assert stride is not None
    assert device is not None
    assert dtype is not None
    return torch.empty_strided(size=size, stride=stride, device=device, dtype=dtype)
