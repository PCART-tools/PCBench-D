def fold(
    input: Tensor,
    output_size: BroadcastingList2[int],
    kernel_size: BroadcastingList2[int],
    dilation: BroadcastingList2[int] = 1,
    padding: BroadcastingList2[int] = 0,
    stride: BroadcastingList2[int] = 1,
) -> Tensor:
    r"""Combine an array of sliding local blocks into a large containing tensor.

    .. warning::
        Currently, only unbatched (3D) or batched (4D) image-like output tensors are supported.

    See :class:`torch.nn.Fold` for details
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            fold,
            (input,),
            input,
            output_size,
            kernel_size,
            dilation=dilation,
            padding=padding,
            stride=stride,
        )
    return torch._C._nn.col2im(
        input,
        _pair(output_size),
        _pair(kernel_size),
        _pair(dilation),
        _pair(padding),
        _pair(stride),
    )
