def create_indices_fake(x) -> torch.Tensor:
    size = [V.graph.sizevars.size_hint(i) for i in x.get_size()]
    indices = torch.arange(0, size[-1], dtype=x.get_dtype(), device=x.get_device())
    indices = indices.expand(size).contiguous()
    return indices
