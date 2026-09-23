def _max_pool_with_indices(
    x: torch.Tensor,
    kernel_size: list[int],
    stride: Optional[Union[int, list[int]]],
    padding: Union[int, list[int]],
    dilation: Union[int, list[int]],
    ceil_mode: bool,
    dim: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    if dilation == 1:
        dilation = [1] * dim

    if padding == 0:
        padding = [0] * dim

    if not stride:
        stride = kernel_size

    kernel_size = pad_listlike(kernel_size, dim)
    dilation = pad_listlike(dilation, dim)
    padding = pad_listlike(padding, dim)
    stride = pad_listlike(stride, dim)

    window_size = functools.reduce(operator.mul, kernel_size)
    # We fallback when using non-default dilation or when the window size is too large
    if (
        torch._inductor.lowering.should_fallback_max_pool_with_indices(
            kernel_size, n_dim=dim
        )
        or window_size > torch.iinfo(torch.int8).max
    ):
        return NotImplemented

    vals, offsets = prims._low_memory_max_pool_with_offsets(
        x,
        kernel_size,
        stride,
        padding,
        dilation,
        ceil_mode,
    )
    indices = prims._low_memory_max_pool_offsets_to_indices(
        offsets,
        kernel_size,
        x.shape[-dim:],
        stride,
        padding,
        dilation,
    )
    return vals, indices
