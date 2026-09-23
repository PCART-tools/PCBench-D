def _detach(x: object) -> object:
    detached: object = None
    if isinstance(x, torch.Tensor):
        detached = x.detach()
    elif isinstance(x, (list, tuple)):
        detached = type(x)([_detach(e) for e in x])
    elif isinstance(x, dict):
        detached = {k: _detach(e) for k, e in x.items()}
    else:
        detached = x
    return detached
