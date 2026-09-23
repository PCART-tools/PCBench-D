def _no_grad_uniform_(
    tensor: Tensor, a: float, b: float, generator: _Optional[torch.Generator] = None
) -> Tensor:
    with torch.no_grad():
        return tensor.uniform_(a, b, generator=generator)
