def partial_apply_nontensors(fn, args, **kwargs):
    source = ['t' if (isinstance(arg, torch.Tensor) or is_iterable_of_tensors(arg)) else 's' for arg in args]

    def new_fn(*tensors_):
        tensors = iter(tensors_)
        return fn(*(args[i] if s == 's' else next(tensors) for i, s in enumerate(source)), **kwargs)

    return new_fn, [arg for arg in args if isinstance(arg, torch.Tensor) or is_iterable_of_tensors(arg)]
