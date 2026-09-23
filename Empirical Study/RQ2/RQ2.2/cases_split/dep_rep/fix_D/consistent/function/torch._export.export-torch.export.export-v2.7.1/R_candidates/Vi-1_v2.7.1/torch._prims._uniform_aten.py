def _uniform_aten(
    shape: ShapeType,
    *,
    low: float,
    high: float,
    dtype: torch.dtype,
    device: torch.device,
    generator: Optional[torch.Generator] = None,
) -> Tensor:
    a = torch.empty(shape, dtype=dtype, device=device)
    a.uniform_(low, high, generator=generator)
    return a
