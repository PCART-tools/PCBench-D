@register_decomposition(aten.addcdiv)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("self", "tensor1", "tensor2"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
)
def addcdiv(
    self: TensorLikeType,
    tensor1: TensorLikeType,
    tensor2: TensorLikeType,
    *,
    value: NumberType = 1,
) -> TensorLikeType:
    """
    Reference implementation of torch.addcdiv
    """
    if value is not None:
        dtype = self.dtype  # no scalars allowed, see add
        python_type = utils.dtype_to_type(dtype)
        torch._check_value(
            utils.is_weakly_lesser_type(type(value), python_type),
            lambda: f"value argument of type {type(value)} cannot be safely cast to type {python_type}!",
        )

    return self + value * tensor1 / tensor2
