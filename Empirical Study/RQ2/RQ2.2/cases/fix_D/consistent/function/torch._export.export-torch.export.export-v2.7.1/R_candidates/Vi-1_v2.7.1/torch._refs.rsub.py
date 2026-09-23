@register_decomposition(aten.rsub)
@out_wrapper()
def rsub(
    a: Union[TensorLikeType, NumberType],
    b: Union[TensorLikeType, NumberType],
    alpha: NumberType = 1,
):
    if isinstance(a, Number):
        msg = "Received a Number for the first argument, but expected a Tensor"
        raise ValueError(msg)

    return torch.sub(b, a, alpha=alpha)
