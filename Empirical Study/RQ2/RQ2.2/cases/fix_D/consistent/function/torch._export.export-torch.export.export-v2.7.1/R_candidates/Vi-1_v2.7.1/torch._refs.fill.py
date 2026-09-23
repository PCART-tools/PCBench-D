@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a,"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.NO_OPMATH,
)
def fill(a: TensorLikeType, value: NumberType) -> TensorLikeType:
    assert isinstance(a, TensorLike)
    assert isinstance(value, Number)

    python_type = utils.dtype_to_type(a.dtype)
    if not utils.is_weakly_lesser_type(type(value), python_type):
        msg = f"value argument of type {type(value)} cannot be safely cast to type {python_type}!"
        raise ValueError(msg)

    return prims.fill(a, value)
