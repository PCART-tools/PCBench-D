@register_function_func([torch.Tensor.contiguous])
def _function_contiguous(func, *args, **kwargs):
    return _MaskedContiguous.apply(args[0])
