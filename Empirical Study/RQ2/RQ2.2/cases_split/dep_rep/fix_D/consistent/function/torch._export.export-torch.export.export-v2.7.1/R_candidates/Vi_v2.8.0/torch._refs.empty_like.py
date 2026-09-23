@register_decomposition(aten.empty_like)
@out_wrapper()
def empty_like(
    a: TensorLikeType,
    *,
    dtype: Optional[torch.dtype] = None,
    device: Optional[DeviceLikeType] = None,
    layout: Optional[torch.layout] = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
    memory_format: torch.memory_format = torch.preserve_format,
) -> TensorLikeType:
    dtype = a.dtype if dtype is None else dtype
    layout = a.layout if layout is None else layout
    device = a.device if device is None else device

    if memory_format != torch.preserve_format:
        return torch.empty(
            a.shape,
            dtype=dtype,
            layout=layout,
            device=device,
            requires_grad=requires_grad,
            pin_memory=pin_memory,
            memory_format=memory_format,
        )

    # memory_format == torch.preserve_format
    logical_to_physical_perm = (
        utils.compute_elementwise_output_logical_to_physical_perm(a)
    )
    # identity perm is [2, 1, 0]
    return torch.empty_permuted(
        a.shape,
        logical_to_physical_perm,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )
