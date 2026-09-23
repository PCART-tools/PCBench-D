@_make_elementwise_binary_reference(
    type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    aten_op=None,  # CompositeImplicitAutograd
    supports_two_python_scalars=True,
)
def trunc_divide(
    a: Union[TensorLikeType, NumberType], b: Union[TensorLikeType, NumberType]
):
    dtype = utils.get_dtype(a)
    if utils.is_integer_dtype(dtype):
        return prims.div(a, b)

    return trunc(prims.div(a, b))
