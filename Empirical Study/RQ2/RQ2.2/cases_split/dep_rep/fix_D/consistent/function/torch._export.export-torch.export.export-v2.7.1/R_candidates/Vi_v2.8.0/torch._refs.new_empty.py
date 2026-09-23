@register_decomposition(aten.new_empty)
@out_wrapper()
def new_empty(
    a: TensorLikeType,
    size: ShapeType,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: Optional[torch.layout] = None,
    device: Optional[DeviceLikeType] = None,
    pin_memory: bool = False,
) -> TensorLikeType:
    dtype = a.dtype if dtype is None else dtype
    layout = a.layout if layout is None else layout
    device = a.device if device is None else device

    return torch.empty(
        size,
        dtype=dtype,
        device=device,
        pin_memory=pin_memory,
        layout=layout,
    )
