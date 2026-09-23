def to_device(i, d):
    if isinstance(i, torch.Tensor):
        return i.to(device=d)
    elif isinstance(i, (tuple, list)):
        return tuple(to_device(e, d) for e in i)
    else:
        raise RuntimeError('inputs are weird')
