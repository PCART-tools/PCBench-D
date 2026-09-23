@register_decomposition(aten.randint_like.low_dtype)
def randint_like_low(
    self: torch.Tensor,
    low: int,
    high: int,
    *,
    dtype: Optional[torch.dtype] = None,
    device: Optional[torch.device] = None,
    memory_format: Optional[torch.memory_format] = None,
    **kwargs: Any,
) -> torch.Tensor:
    return aten.randint.low(
        low,
        high,
        [*self.size()],
        dtype=dtype or self.dtype,
        device=device or self.device,
        **kwargs,
    ).to(memory_format=get_like_layout(self, memory_format))
