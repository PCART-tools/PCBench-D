@register_dispatch_func([torch.ops.aten.contiguous])
def contiguous(func, *args, **kwargs):
    if _get_data(args[0]).is_sparse:
        raise ValueError("MaskedTensors with sparse data do not have contiguous")
    return _MaskedContiguous.apply(args[0])
