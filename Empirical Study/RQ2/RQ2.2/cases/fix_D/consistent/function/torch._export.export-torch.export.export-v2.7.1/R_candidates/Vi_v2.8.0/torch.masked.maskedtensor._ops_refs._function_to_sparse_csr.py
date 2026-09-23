@register_function_func([torch.Tensor.to_sparse_csr])
def _function_to_sparse_csr(func, *args, **kwargs):
    return _MaskedToSparseCsr.apply(args[0])
