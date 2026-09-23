def conv1d_weight(input, weight_size, grad_output, stride=1, padding=0, dilation=1, groups=1):
    r"""
    Computes the gradient of conv1d with respect to the weight of the convolution.

    Args:
        input: input tensor of shape (minibatch x in_channels x iW)
        weight_size : Shape of the weight gradient tensor
        grad_output : output gradient tensor (minibatch x out_channels x oW)
        stride (int or tuple, optional): Stride of the convolution. Default: 1
        padding (int or tuple, optional): Zero-padding added to both sides of the input. Default: 0
        dilation (int or tuple, optional): Spacing between kernel elements. Default: 1
        groups (int, optional): Number of blocked connections from input channels to output channels. Default: 1

    Examples::

        >>> input = torch.randn(1,1,3, requires_grad=True)
        >>> weight = torch.randn(1,1,1, requires_grad=True)
        >>> output = F.conv1d(input, weight)
        >>> grad_output = torch.randn(output.shape)
        >>> grad_weight = torch.autograd.grad(output, filter, grad_output)
        >>> F.grad.conv1d_weight(input, weight.shape, grad_output)

    """
    stride = _single(stride)
    padding = _single(padding)
    dilation = _single(dilation)
    in_channels = input.shape[1]
    out_channels = grad_output.shape[1]
    min_batch = input.shape[0]

    grad_output = grad_output.contiguous().repeat(1, in_channels // groups, 1)
    grad_output = grad_output.contiguous().view(
        grad_output.shape[0] * grad_output.shape[1], 1, grad_output.shape[2])

    input = input.contiguous().view(1, input.shape[0] * input.shape[1],
                                    input.shape[2])

    grad_weight = torch.conv1d(input, grad_output, None, dilation, padding,
                               stride, in_channels * min_batch)

    grad_weight = grad_weight.contiguous().view(
        min_batch, grad_weight.shape[1] // min_batch, grad_weight.shape[2])

    return grad_weight.sum(dim=0).view(
        in_channels // groups, out_channels, grad_weight.shape[2]).transpose(
            0, 1).narrow(2, 0, weight_size[2])
