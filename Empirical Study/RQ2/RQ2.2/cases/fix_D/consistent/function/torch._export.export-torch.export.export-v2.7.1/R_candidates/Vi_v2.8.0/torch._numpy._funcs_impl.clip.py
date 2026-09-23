def clip(
    a: ArrayLike,
    min: Optional[ArrayLike] = None,
    max: Optional[ArrayLike] = None,
    out: Optional[OutArray] = None,
):
    return torch.clamp(a, min, max)
