@register_decomposition(aten.bernoulli.default)
def bernoulli(
    self: torch.Tensor,
    *,
    generator: Optional[torch.Generator] = None,
) -> torch.Tensor:
    if generator is None:
        raw_p = torch.rand(self.size(), dtype=torch.float32, device=self.device)
    else:
        raw_p = torch.rand(
            self.size(),
            generator=generator,
            dtype=torch.float32,
            device=self.device,
        )
    p = (raw_p < self).to(self.dtype)
    return p
