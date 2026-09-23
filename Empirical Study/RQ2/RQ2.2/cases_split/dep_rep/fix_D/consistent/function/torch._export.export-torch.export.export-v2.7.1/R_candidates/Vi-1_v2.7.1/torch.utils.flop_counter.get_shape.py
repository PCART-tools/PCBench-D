def get_shape(i):
    if isinstance(i, torch.Tensor):
        return i.shape
    return i
