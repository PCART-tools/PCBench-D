@register_decomposition(aten.new_empty_strided)
@out_wrapper()
def new_empty_strided(
    a: TensorLikeType,
    size: ShapeType,
    stride: StrideType,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: Optional[torch.layout] = None,
    device: Optional[DeviceLikeType] = None,
    pin_memory: bool = False,
) -> TensorLikeType:
    """
    Reference implementation of torch.Tensor.new_empty_strided
    """

    dtype = a.dtype if dtype is None else dtype
    layout = a.layout if layout is None else layout
    device = a.device if device is None else device

    return torch.empty_strided(
        size,
        stride,
        dtype=dtype,
        device=device,
        pin_memory=pin_memory,
        layout=layout,
    )
