@register_decomposition(aten.eye)
@out_wrapper()
def eye(
    n: int,
    m: Optional[int] = None,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[DeviceLikeType] = None,
    pin_memory: bool = False,
    requires_grad: bool = False,  # TODO: unused
) -> TensorLikeType:
    """
    Reference implementation of torch.eye
    """
    if m is None:
        m = n

    torch._check(n >= 0, lambda: f"n must be greater or equal to 0, got {n}")
    torch._check(m >= 0, lambda: f"m must be greater or equal to 0, got {m}")

    range_n = torch.arange(n, dtype=torch.int64, device=device, requires_grad=False)
    range_m = torch.arange(m, dtype=torch.int64, device=device, requires_grad=False)

    cond = range_n.unsqueeze(-1) == range_m
    if dtype is torch.bool:
        return cond
    else:
        one = torch.ones(
            (1,),
            dtype=dtype,
            layout=layout,
            device=device,
            pin_memory=pin_memory,
            requires_grad=False,
        )
        return torch.where(cond, one, 0)
