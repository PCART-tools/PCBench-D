def full_like(
    a: TensorLikeType,
    fill_value: NumberType,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: Optional[torch.layout] = None,
    device: Optional[DeviceLikeType] = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
    memory_format: torch.memory_format = torch.preserve_format,
) -> TensorLikeType:
    e = torch.empty_like(
        a,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
        memory_format=memory_format,
    )
    return fill(e, fill_value)
