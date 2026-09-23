def variable(*args, **kwargs):
    warnings.warn("torch.autograd.variable(...) is deprecated, use torch.tensor(...) instead")
    return torch.tensor(*args, **kwargs)
