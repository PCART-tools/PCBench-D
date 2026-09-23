@register_decomposition(aten.special_xlog1py)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a", "b"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
)
def xlog1py(a: Union[TensorLikeType, NumberType], b: Union[TensorLikeType, NumberType]):
    torch._check(
        isinstance(a, TensorLike) or isinstance(b, TensorLike),
        lambda: 'Expected either argument a or b to be a Tensor"',
    )

    # Operations like eq and log do not handle scalar values, so we convert them to scalar_tensors.
    if isinstance(a, TensorLike) and isinstance(b, Number):
        b = refs.scalar_tensor(b, dtype=a.dtype, device=a.device)
    elif isinstance(b, TensorLike) and isinstance(a, Number):
        a = refs.scalar_tensor(a, dtype=b.dtype, device=b.device)

    # mypy: expected "Tensor"
    assert isinstance(a, TensorLike)
    assert isinstance(b, TensorLike)
    rhs = torch.where(torch.eq(a, 0), 0, torch.mul(a, torch.log1p(b)))
    return torch.where(torch.isnan(b), float("nan"), rhs)
