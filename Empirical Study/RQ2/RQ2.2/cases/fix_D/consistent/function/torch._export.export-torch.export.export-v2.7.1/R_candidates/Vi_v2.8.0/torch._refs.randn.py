@register_decomposition(aten.randn.default)
@out_wrapper()
def randn(
    *shape,
    dtype: Optional[torch.dtype] = None,
    device: Optional[DeviceLikeType] = None,
    layout: Optional[torch.layout] = None,
    requires_grad: bool = False,
    pin_memory: bool = False,
) -> TensorLikeType:
    utils.check_pin_memory(pin_memory)

    shape_ = utils.extract_shape_from_varargs(shape)

    dtype = utils.dtype_or_default(dtype)
    device = utils.device_or_default(device)

    return prims.normal(
        shape_,
        mean=0.0,
        std=1.0,
        dtype=dtype,
        device=device,
        requires_grad=requires_grad,
    )
