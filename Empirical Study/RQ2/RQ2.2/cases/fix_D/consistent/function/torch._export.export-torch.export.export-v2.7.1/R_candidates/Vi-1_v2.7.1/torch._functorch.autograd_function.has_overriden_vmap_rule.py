def has_overriden_vmap_rule(autograd_function):
    return autograd_function.vmap is not torch.autograd.Function.vmap
