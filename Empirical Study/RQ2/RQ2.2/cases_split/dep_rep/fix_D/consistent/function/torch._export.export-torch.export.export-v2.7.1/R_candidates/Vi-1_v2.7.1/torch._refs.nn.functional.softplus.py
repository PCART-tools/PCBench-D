@register_decomposition(aten.softplus)
@_inplace_wrapper
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a",),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def softplus(
    a: TensorLikeType,
    beta: Optional[NumberType] = None,
    threshold: NumberType = 20,
    inplace: bool = False,
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.softplus
    """

    if inplace:
        raise NotImplementedError

    rhs: TensorLikeType
    if beta is not None:
        python_type = utils.dtype_to_type(a.dtype)
        if not utils.is_weakly_lesser_type(type(beta), python_type):
            msg = f"beta argument of type {type(beta)} cannot be safely cast to type {python_type}!"
            raise ValueError(msg)
        scaled_input = a * beta
        rhs = torch.true_divide(torch.log1p(torch.exp(scaled_input)), beta)  # type: ignore[arg-type]

    else:
        scaled_input = a
        rhs = torch.log1p(torch.exp(scaled_input))

    return torch.where(scaled_input > threshold, a, rhs)
