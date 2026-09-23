@register_decomposition(aten.full_like)
def full_like(
    self: torch.Tensor,
    fill_value: Union[int, float],
    *,
    dtype: Optional[torch.dtype] = None,
    layout: Optional[torch.layout] = None,
    device: Optional[torch.device] = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
    memory_format: torch.memory_format = torch.preserve_format,
) -> torch.Tensor:
    return torch.full(
        [*self.size()],
        fill_value,
        dtype=dtype or self.dtype,
        layout=layout or self.layout,
        device=device or self.device,
        requires_grad=requires_grad,
    ).to(memory_format=get_like_layout(self, memory_format))
