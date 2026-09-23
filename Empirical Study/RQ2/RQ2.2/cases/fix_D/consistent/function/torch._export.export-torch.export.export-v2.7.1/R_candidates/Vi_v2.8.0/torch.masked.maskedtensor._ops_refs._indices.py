@register_dispatch_func([torch.ops.aten._indices])
def _indices(func, *args, **kwargs):
    # Assumes data is sparse
    _check_args_kwargs_length(
        args, kwargs, f"__torch_dispatch__, {func}", len_args=1, len_kwargs=0
    )
    data = _get_data(args[0]).indices()
    return MaskedTensor(data, torch.ones_like(data).bool())
