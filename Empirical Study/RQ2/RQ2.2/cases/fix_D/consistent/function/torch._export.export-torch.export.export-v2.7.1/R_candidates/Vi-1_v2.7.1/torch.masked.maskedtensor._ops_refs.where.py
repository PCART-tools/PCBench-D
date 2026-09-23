@register_dispatch_func([torch.ops.aten.where])
def where(func, *args, **kwargs):
    _check_args_kwargs_length(
        args, kwargs, f"__torch_dispatch__, {func}", len_args=3, len_kwargs=0
    )
    if not torch.is_tensor(args[0]):
        raise ValueError("__torch_dispatch__, {func}: expected args[0] to be a tensor")
    mx = args[1]
    my = args[2]
    if not is_masked_tensor(mx):
        mx = MaskedTensor(mx, torch.ones_like(mx, dtype=torch.bool))
    if not is_masked_tensor(my):
        my = MaskedTensor(my, torch.ones_like(my, dtype=torch.bool))
    new_data = func(args[0], mx.get_data(), my.get_data())
    new_mask = func(args[0], mx.get_mask(), my.get_mask())
    return MaskedTensor(new_data, new_mask)
