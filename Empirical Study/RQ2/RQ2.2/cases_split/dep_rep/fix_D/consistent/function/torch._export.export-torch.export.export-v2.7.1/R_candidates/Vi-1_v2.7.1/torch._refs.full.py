@register_decomposition([aten.full.default, aten.full.out])
@out_wrapper()
def full(
    shape: ShapeType,
    fill_value: NumberType,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[DeviceLikeType] = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
) -> TensorLikeType:
    utils.check_layout(layout)
    utils.check_pin_memory(pin_memory)

    dtype = dtype if dtype is not None else utils.type_to_dtype(type(fill_value))
    device = device if device is not None else torch.device("cpu")

    e = empty(
        shape,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )
    return torch.fill(e, fill_value)  # type: ignore[arg-type]
