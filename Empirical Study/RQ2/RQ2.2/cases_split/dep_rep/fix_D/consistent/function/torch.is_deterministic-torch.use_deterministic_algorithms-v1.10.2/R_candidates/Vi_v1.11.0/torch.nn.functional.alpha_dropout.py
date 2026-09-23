def alpha_dropout(input: Tensor, p: float = 0.5, training: bool = False, inplace: bool = False) -> Tensor:
    r"""Applies alpha dropout to the input.

    See :class:`~torch.nn.AlphaDropout` for details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(alpha_dropout, (input,), input, p=p, training=training, inplace=inplace)
    if p < 0.0 or p > 1.0:
        raise ValueError("dropout probability has to be between 0 and 1, " "but got {}".format(p))
    return _VF.alpha_dropout_(input, p, training) if inplace else _VF.alpha_dropout(input, p, training)
