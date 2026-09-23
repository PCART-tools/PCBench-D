@register_decomposition(aten.new_full)
@out_wrapper()
def new_full(
    a: TensorLikeType,
    size: ShapeType,
    fill_value: NumberType,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: Optional[torch.layout] = None,
    device: Optional[DeviceLikeType] = None,
    pin_memory: bool = False,
) -> TensorLikeType:
    dtype = a.dtype if dtype is None else dtype
    layout = a.layout if layout is None else layout
    device = a.device if device is None else device

    return torch.full(
        size,
        fill_value,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
    )
