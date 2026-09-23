@register_decomposition(aten.sub)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a", "b"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def sub(
    a: Union[TensorLikeType, NumberType],
    b: Union[TensorLikeType, NumberType],
    *,
    alpha: NumberType = 1,
):
    """
    Reference implementation of torch.sub
    """

    a, b = _maybe_broadcast(a, b)

    if isinstance(a, TensorLike) and isinstance(b, TensorLike):
        torch._check(
            not utils.is_boolean_dtype(a.dtype) and not utils.is_boolean_dtype(b.dtype),
            lambda: (
                "Subtraction, the `-` operator, with two bool tensors is not supported. "
                "Use the `^` or `logical_xor()` operator instead."
            ),
        )

    if alpha != 1:
        dtype = a.dtype if isinstance(a, TensorLike) else b.dtype  # type: ignore[union-attr]
        python_type = utils.dtype_to_type(dtype)
        if not utils.is_weakly_lesser_type(type(alpha), python_type):
            msg = f"alpha argument of type {type(alpha)} cannot be safely cast to type {python_type}!"
            raise ValueError(msg)
        if isinstance(b, torch.Tensor):
            b = prims.mul(b, alpha)
        else:
            # Carefully not to use prims.mul if b is a scalar / symint.
            # prims.mul always returns a tensor,
            # which will mess with type promotion.
            b = b * alpha

    output = prims.sub(a, b)
    return handle_noncontiguous_outputs([a, b], output)
