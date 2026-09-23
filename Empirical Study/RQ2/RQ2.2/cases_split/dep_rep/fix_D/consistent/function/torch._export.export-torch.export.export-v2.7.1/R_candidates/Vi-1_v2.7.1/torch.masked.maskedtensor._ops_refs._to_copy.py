@register_dispatch_func([torch.ops.aten._to_copy])
def _to_copy(func, *args, **kwargs):
    new_data = func(_get_data(args[0]), *args[1:], **kwargs)
    return MaskedTensor(new_data, _maybe_get_mask(args[0]))
