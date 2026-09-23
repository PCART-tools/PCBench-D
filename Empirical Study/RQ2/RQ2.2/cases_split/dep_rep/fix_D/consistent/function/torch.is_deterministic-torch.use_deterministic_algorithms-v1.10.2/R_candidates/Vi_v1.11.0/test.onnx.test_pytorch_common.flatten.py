def flatten(x):
    return tuple(function._iter_filter(lambda o: isinstance(o, torch.Tensor))(x))
