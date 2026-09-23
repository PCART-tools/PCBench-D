@register_decomposition(aten.max_pool2d_with_indices)
def max_pool2d_with_indices(
    x: torch.Tensor,
    kernel_size: list[int],
    stride: Optional[Union[int, list[int]]] = None,
    padding: Union[int, list[int]] = 0,
    dilation: Union[int, list[int]] = 1,
    ceil_mode: bool = False,
) -> tuple[torch.Tensor, torch.Tensor]:
    if dilation == 1:
        dilation = [1, 1]

    if padding == 0:
        padding = [0, 0]

    if not stride:
        stride = kernel_size

    kernel_size = pad_listlike(kernel_size, 2)
    dilation = pad_listlike(dilation, 2)
    padding = pad_listlike(padding, 2)
    stride = pad_listlike(stride, 2)

    window_size = kernel_size[0] * kernel_size[1]
    # We fallback when using non-default dilation or when the window size is too large
    if (
        torch._inductor.lowering.should_fallback_max_pool2d_with_indices(
            kernel_size, dilation
        )
        or window_size > torch.iinfo(torch.int8).max
    ):
        return NotImplemented

    vals, offsets = prims._low_memory_max_pool2d_with_offsets(
        x,
        kernel_size,
        stride,
        padding,
        dilation,
        ceil_mode,
    )
    indices = prims._low_memory_max_pool2d_offsets_to_indices(
        offsets,
        kernel_size[1],
        x.size(-1),
        stride,
        padding,
    )
    return vals, indices
