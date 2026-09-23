@register_decomposition(aten.randn_like)
def randn_like(
    self: torch.Tensor,
    *,
    dtype: Optional[torch.dtype] = None,
    device: Optional[torch.device] = None,
    memory_format: Optional[torch.memory_format] = None,
    **kwargs: Any,
) -> torch.Tensor:
    return torch.randn(
        [*self.size()],
        dtype=dtype or self.dtype,
        device=device or self.device,
        **kwargs,
    ).to(memory_format=get_like_layout(self, memory_format))
