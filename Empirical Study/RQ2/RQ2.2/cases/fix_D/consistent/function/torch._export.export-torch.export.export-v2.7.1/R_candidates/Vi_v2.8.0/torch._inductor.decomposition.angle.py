@register_decomposition([aten.angle])
def angle(x: torch.Tensor) -> torch.Tensor:
    if x.is_complex():
        return torch.where(
            torch.isnan(x.real), float("nan"), torch.atan2(x.imag, x.real)
        )

    # when x is real number
    #   if x >= 0, return 0
    #   if x < 0, return pi
    #   if x is nan, return nan
    _, dtype = elementwise_dtypes(
        x,
        type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
    )
    pi = torch.scalar_tensor(math.pi, dtype=dtype, device=x.device)
    ret = torch.where(x < 0, pi, 0.0)
    return torch.where(torch.isnan(x), float("nan"), ret)
