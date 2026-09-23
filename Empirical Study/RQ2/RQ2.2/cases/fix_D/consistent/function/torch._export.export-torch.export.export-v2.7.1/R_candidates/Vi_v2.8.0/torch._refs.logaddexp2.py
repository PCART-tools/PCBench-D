@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    supports_lhs_python_scalar=False,
    supports_rhs_python_scalar=False,
)
def logaddexp2(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    torch._check(
        not (utils.is_complex_dtype(a.dtype) or utils.is_complex_dtype(b.dtype)),
        lambda: "logaddexp2 doesn't support complex dtypes",
    )
    # Nb. this implementation does not distribute the gradients evenly when a == b
    mask = a >= b
    max_ = torch.where(mask, a, b)
    min_ = torch.where(mask, b, a)
    inf_mask = torch.logical_and(torch.isinf(a), a == b)
    inv_log_2 = 1.0 / math.log(2)
    result = max_ + torch.log1p(torch.exp2(min_ - max_)) * inv_log_2
    return torch.where(inf_mask, a, result)
