def expand_as(a: Tensor, b: Tensor) -> Tensor:
    return a.expand(b.shape)
