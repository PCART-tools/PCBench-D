@register_dispatch_func([torch.ops.aten.is_contiguous])
def is_contiguous(func, *args, **kwargs):
    data = _get_data(args[0])
    if data.is_sparse:
        raise ValueError("MaskedTensors with sparse data do not have is_contiguous")
    return func(data, *args[1:], **kwargs)
