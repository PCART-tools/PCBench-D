def unfold(
    input: Tensor,
    kernel_size: BroadcastingList2[int],
    dilation: BroadcastingList2[int] = 1,
    padding: BroadcastingList2[int] = 0,
    stride: BroadcastingList2[int] = 1,
) -> Tensor:
    r"""Extract sliding local blocks from a batched input tensor.

    .. warning::
        Currently, only 4-D input tensors (batched image-like tensors) are
        supported.

    .. warning::

        More than one element of the unfolded tensor may refer to a single
        memory location. As a result, in-place operations (especially ones that
        are vectorized) may result in incorrect behavior. If you need to write
        to the tensor, please clone it first.


    See :class:`torch.nn.Unfold` for details
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            unfold,
            (input,),
            input,
            kernel_size,
            dilation=dilation,
            padding=padding,
            stride=stride,
        )
    return torch._C._nn.im2col(
        input, _pair(kernel_size), _pair(dilation), _pair(padding), _pair(stride)
    )
