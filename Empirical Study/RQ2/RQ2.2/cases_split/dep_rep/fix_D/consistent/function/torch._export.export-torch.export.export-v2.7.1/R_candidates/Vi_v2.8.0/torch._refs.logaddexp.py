@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    supports_lhs_python_scalar=False,
    supports_rhs_python_scalar=False,
)
def logaddexp(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    # Nb. this implementation does not distribute the gradients evenly when a == b
    mask = torch.real(a) >= torch.real(b)
    max_ = torch.where(mask, a, b)
    min_ = torch.where(mask, b, a)
    inf_mask = torch.logical_and(
        torch.logical_not(torch.isfinite(torch.real(a))), torch.real(a) == torch.real(b)
    )
    if utils.is_complex_dtype(a.dtype) or utils.is_complex_dtype(b.dtype):
        # are you wondering what this bunch of codes are for? edge cases!
        neg_min_mask = torch.real(min_) < 0
        inf_vals = torch.where(
            neg_min_mask, min_, torch.log(torch.exp(min_) + torch.exp(max_))
        )
        non_nan_vals = torch.where(
            inf_mask, inf_vals, max_ + torch.log1p(torch.exp(min_ - max_))
        )
        # the type for full_like does not include tensor yet
        nan_mask = torch.isnan(min_)
        return torch.where(nan_mask, complex(float("nan"), float("nan")), non_nan_vals)  # type: ignore[call-overload]
    else:
        return torch.where(inf_mask, a, max_ + torch.log1p(torch.exp(min_ - max_)))
