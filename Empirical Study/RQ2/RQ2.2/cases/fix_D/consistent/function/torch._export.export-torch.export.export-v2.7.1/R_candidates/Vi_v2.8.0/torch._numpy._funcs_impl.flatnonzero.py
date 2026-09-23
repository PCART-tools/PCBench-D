def flatnonzero(a: ArrayLike):
    return torch.flatten(a).nonzero(as_tuple=True)[0]
