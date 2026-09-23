def build_constraint(constraint_fn, args, is_cuda=False):
    if not args:
        return constraint_fn
    t = torch.cuda.DoubleTensor if is_cuda else torch.DoubleTensor
    return constraint_fn(*(t(x) if isinstance(x, list) else x for x in args))
