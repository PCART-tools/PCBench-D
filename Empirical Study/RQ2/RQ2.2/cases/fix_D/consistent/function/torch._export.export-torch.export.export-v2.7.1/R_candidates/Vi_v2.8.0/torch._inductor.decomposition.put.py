@register_decomposition(aten.put)
def put(
    self: torch.Tensor,
    index: torch.Tensor,
    source: torch.Tensor,
    accumulate: bool = False,
) -> torch.Tensor:
    flattened = self.flatten()
    flattened = torch.index_put(
        flattened, [index], source.reshape(index.shape), accumulate
    )
    return flattened.reshape(self.shape)
