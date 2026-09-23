def wrap(v):
    if type(v) in {tuple, list}:
        return type(v)(wrap(vi) for vi in v)

    return Wrapper(v) if isinstance(v, torch.Tensor) else v
