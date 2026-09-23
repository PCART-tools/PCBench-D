def scalar_tensor(
    a: NumberType,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[DeviceLikeType] = None,
    pin_memory: bool = False,
) -> TensorLikeType:
    utils.check_layout(layout)
    utils.check_pin_memory(pin_memory)
    dtype = dtype if dtype is not None else utils.type_to_dtype(type(a))
    device = device if device is not None else torch.device("cpu")
    return prims.scalar_tensor(a, dtype=dtype, device=device)
