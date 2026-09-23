def fold(
    input: Tensor, output_size: BroadcastingList2[int],
    kernel_size: BroadcastingList2[int],
    dilation: BroadcastingList2[int] = 1,
    padding: BroadcastingList2[int] = 0,
    stride: BroadcastingList2[int] = 1
) -> Tensor:
    r"""Combines an array of sliding local blocks into a large containing
    tensor.

    .. warning::
        Currently, only unbatched (3D) or batched (4D) image-like output tensors are supported.

    See :class:`torch.nn.Fold` for details
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            fold, (input,), input, output_size, kernel_size, dilation=dilation, padding=padding, stride=stride
        )
    if input.dim() == 3 or input.dim() == 2:
        msg = "{} must be int or 2-tuple for 3D input"
        assert_int_or_pair(output_size, "output_size", msg)
        assert_int_or_pair(kernel_size, "kernel_size", msg)
        assert_int_or_pair(dilation, "dilation", msg)
        assert_int_or_pair(padding, "padding", msg)
        assert_int_or_pair(stride, "stride", msg)

        return torch._C._nn.col2im(
            input, _pair(output_size), _pair(kernel_size), _pair(dilation), _pair(padding), _pair(stride)
        )
    else:
        raise NotImplementedError("Input Error: Only unbatched (2D) or batched (3D) input Tensors"
                                  f"are supported (got {input.dim()}D)")
