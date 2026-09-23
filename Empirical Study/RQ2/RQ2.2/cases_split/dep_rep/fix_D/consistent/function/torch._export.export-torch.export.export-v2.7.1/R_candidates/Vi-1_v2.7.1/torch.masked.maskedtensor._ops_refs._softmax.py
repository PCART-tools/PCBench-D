@register_dispatch_func([torch.ops.aten._softmax])
def _softmax(func, *args, **kwargs):
    _check_args_kwargs_length(
        args, kwargs, f"__torch_dispatch__, {func}", len_args=3, len_kwargs=0
    )
    data = _get_data(args[0])
    mask = _maybe_get_mask(args[0])
    result_data = torch.ops.aten._masked_softmax(data, ~mask, args[1], 2)
    return MaskedTensor(result_data, mask)
