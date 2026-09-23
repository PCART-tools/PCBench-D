def clone_preserve_strides(x: torch.Tensor) -> torch.Tensor:
    if 0 in x.size():
        # Short-circuits if the shape has no elements
        needed_size = 0
    else:
        needed_size = (
            sum((shape - 1) * stride for shape, stride in zip(x.size(), x.stride())) + 1
        )
    buffer = torch.as_strided(x, (needed_size,), (1,)).clone()
    return torch.as_strided(buffer, x.size(), x.stride())
