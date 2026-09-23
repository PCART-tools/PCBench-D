def increment_version(val: Any) -> None:
    if isinstance(val, Tensor):
        torch.autograd.graph.increment_version(val)
    elif isinstance(val, (tuple, list)):
        for v in val:
            if isinstance(v, Tensor):
                torch.autograd.graph.increment_version(v)
