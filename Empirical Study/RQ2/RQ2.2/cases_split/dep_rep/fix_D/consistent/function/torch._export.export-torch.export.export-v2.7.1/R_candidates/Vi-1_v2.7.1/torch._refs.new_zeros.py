@register_decomposition(aten.new_zeros)
@out_wrapper()
def new_zeros(
    a: TensorLikeType,
    size: ShapeType,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: Optional[torch.layout] = None,
    device: Optional[DeviceLikeType] = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
) -> TensorLikeType:
    dtype = a.dtype if dtype is None else dtype
    layout = a.layout if layout is None else layout
    device = a.device if device is None else device

    return torch.full(
        size,
        False if (dtype or a.dtype) == torch.bool else 0,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )
