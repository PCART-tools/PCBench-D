def glu(input: Tensor, dim: int = -1) -> Tensor:
    r"""
    glu(input, dim=-1) -> Tensor

    The gated linear unit. Computes:

    .. math ::
        \text{GLU}(a, b) = a \otimes \sigma(b)

    where `input` is split in half along `dim` to form `a` and `b`, :math:`\sigma`
    is the sigmoid function and :math:`\otimes` is the element-wise product between matrices.

    See `Language Modeling with Gated Convolutional Networks <https://arxiv.org/abs/1612.08083>`_.

    Args:
        input (Tensor): input tensor
        dim (int): dimension on which to split the input. Default: -1
    """
    if has_torch_function_unary(input):
        return handle_torch_function(glu, (input,), input, dim=dim)
    if input.dim() == 0:
        raise RuntimeError("glu does not support scalars because halving size must be even")
    return torch._C._nn.glu(input, dim)
