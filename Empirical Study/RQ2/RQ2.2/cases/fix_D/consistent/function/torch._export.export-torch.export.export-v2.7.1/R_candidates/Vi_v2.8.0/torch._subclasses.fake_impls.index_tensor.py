@register_op_impl(aten.index.Tensor)
def index_tensor(fake_mode, func, *args, **kwargs):
    from torch._meta_registrations import meta_index_Tensor

    _, new_kwargs = normalize_function(
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    out_device = new_kwargs["input"].device
    # ensure nonzero call goes to fake tensor
    with fake_mode:
        out = meta_index_Tensor(*args, **kwargs)
        return out.to(out_device)
