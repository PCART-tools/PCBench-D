@register_decomposition(aten.empty_strided)
@out_wrapper()
def empty_strided(
    shape: Union[ShapeType, tuple[ShapeType]],
    strides: StrideType,
    *,
    dtype: Optional[torch.dtype] = None,
    device: Optional[DeviceLikeType] = None,
    layout: torch.layout = torch.strided,
    requires_grad: bool = False,
    pin_memory: bool = False,
) -> TensorLikeType:
    # Layout == strided, pin_memory is False
    utils.check_layout(layout)
    utils.check_pin_memory(pin_memory)

    shape = utils.extract_shape_from_varargs(shape)
    dtype = torch.get_default_dtype() if dtype is None else dtype
    device = torch.device("cpu") if device is None else device

    return prims.empty_strided(
        shape,
        strides,
        dtype=dtype,
        device=device,
        requires_grad=requires_grad,
    )
