@register_lowering(aten.new_empty_strided)
def new_empty_strided(
    x, size, stride, *, dtype=None, layout=None, device=None, pin_memory=None
):
    if dtype is None:
        dtype = x.get_dtype()
    if device is None:
        device = x.get_device()
    return empty_strided(
        size,
        stride,
        dtype=dtype,
        layout=layout,
        device=decode_device(device),
        pin_memory=pin_memory,
    )
