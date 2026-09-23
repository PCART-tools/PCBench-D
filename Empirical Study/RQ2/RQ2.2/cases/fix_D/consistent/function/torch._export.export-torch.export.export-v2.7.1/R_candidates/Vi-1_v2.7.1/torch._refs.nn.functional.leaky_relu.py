@register_decomposition(aten.leaky_relu)
@_inplace_wrapper
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a",),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def leaky_relu(
    a: TensorLikeType, negative_slope: float = 0.01, inplace: bool = False
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.leaky_relu
    """

    if inplace:
        raise NotImplementedError

    python_type = utils.dtype_to_type(a.dtype)
    if not utils.is_weakly_lesser_type(type(negative_slope), python_type):
        msg = f"negative_slope argument of type {type(negative_slope)} cannot be safely cast to type {python_type}!"
        raise ValueError(msg)
    return torch.where(torch.gt(a, 0), a, torch.mul(a, negative_slope))
