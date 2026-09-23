def conv3d_input(input_size, weight, grad_output, stride=1, padding=0, dilation=1, groups=1):
    r"""
    Computes the gradient of conv3d with respect to the input of the convolution.
    This is same as the 3D transposed convolution operator under the hood but requires
    the shape of the gradient w.r.t. input to be specified explicitly.

    Args:
        input_size : Shape of the input gradient tensor
        weight: weights tensor (out_channels x in_channels/groups x kT x kH x kW)
        grad_output : output gradient tensor (minibatch x out_channels x oT x oH x oW)
        stride (int or tuple, optional): Stride of the convolution. Default: 1
        padding (int or tuple, optional): Zero-padding added to both sides of the input. Default: 0
        dilation (int or tuple, optional): Spacing between kernel elements. Default: 1
        groups (int, optional): Number of blocked connections from input channels to output channels. Default: 1

    Examples::

        >>> input = torch.randn(2, 8, 10, 10, 20, requires_grad=True)
        >>> weight = torch.randn(4, 8, 2, 3, 3, requires_grad=True)
        >>> output = F.conv3d(input, weight)
        >>> grad_output = torch.randn(output.shape)
        >>> grad_input = torch.autograd.grad(output, input, grad_output)
        >>> F.grad.conv3d_input(input.shape, weight, grad_output)

    """
    stride = _triple(stride)
    padding = _triple(padding)
    dilation = _triple(dilation)
    kernel_size = (weight.shape[2], weight.shape[3], weight.shape[4])

    if input_size is None:
        raise ValueError("grad.conv3d_input requires specifying an input_size")

    grad_input_padding = _grad_input_padding(grad_output, input_size, stride,
                                             padding, kernel_size, dilation)

    return torch.conv_transpose3d(
        grad_output, weight, None, stride, padding, grad_input_padding, groups,
        dilation)
