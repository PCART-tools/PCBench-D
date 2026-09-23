@register_decomposition(aten.zeros.default)
@out_wrapper()
def zeros(
    *size,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[DeviceLikeType] = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
) -> TensorLikeType:
    size = utils.extract_shape_from_varargs(size)

    if dtype is None:
        dtype = torch.get_default_dtype()

    return torch.full(
        size,
        False if dtype == torch.bool else 0,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )
