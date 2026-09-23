@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
    name="true_divide",
    aten_op=None,  # CompositeImplicitAutograd
    supports_two_python_scalars=True,
)
def true_divide(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.div(a, b)
