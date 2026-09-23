@out_wrapper()
def empty(
    *shape,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[DeviceLikeType] = None,
    requires_grad: bool = False,
    pin_memory: bool = False,
    memory_format: torch.memory_format = torch.contiguous_format,
) -> TensorLikeType:
    torch._check(
        memory_format != torch.preserve_format,
        lambda: "torch.empty: the Preserve memory format is not supported",
    )

    shape = utils.extract_shape_from_varargs(shape)

    if memory_format == torch.contiguous_format:
        strides = utils.make_contiguous_strides_for(shape)
    elif memory_format == torch.channels_last_3d:
        strides = utils.make_channels_last_3d_strides_for(shape)
    else:  # memory_format == torch.channels_last
        torch._check(
            memory_format == torch.channels_last,
            lambda: f"torch.empty: received an unknown memory format {memory_format}!",
        )
        strides = utils.make_channels_last_2d_strides_for(shape)

    return torch.empty_strided(
        shape,
        strides,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )
