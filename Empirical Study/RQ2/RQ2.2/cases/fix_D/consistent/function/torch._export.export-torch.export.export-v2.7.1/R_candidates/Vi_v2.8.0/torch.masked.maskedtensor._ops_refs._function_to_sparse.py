@register_function_func([torch.Tensor.to_sparse])
def _function_to_sparse(func, *args, **kwargs):
    return _MaskedToSparse.apply(args[0])
