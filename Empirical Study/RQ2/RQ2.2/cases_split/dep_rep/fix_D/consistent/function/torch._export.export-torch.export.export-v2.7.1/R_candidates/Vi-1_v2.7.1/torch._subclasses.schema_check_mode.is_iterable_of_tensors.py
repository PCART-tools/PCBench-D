def is_iterable_of_tensors(iterable):
    # Tensor itself is iterable so we check this first
    if isinstance(iterable, torch.Tensor):
        return False
    try:
        if len(iterable) == 0:
            return False
        for t in iter(iterable):
            if not isinstance(t, torch.Tensor):
                return False
    except TypeError:
        return False
    return True
