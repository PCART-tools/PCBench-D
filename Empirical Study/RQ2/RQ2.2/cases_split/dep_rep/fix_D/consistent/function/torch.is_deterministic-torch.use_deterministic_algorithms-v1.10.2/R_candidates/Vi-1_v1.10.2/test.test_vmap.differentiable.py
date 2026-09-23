def differentiable(args):
    return tuple(arg for arg in as_tuple(args)
                 if isinstance(arg, torch.Tensor) and arg.requires_grad)
