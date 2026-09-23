@register_dispatch_func([torch.ops.aten.stride])
def stride(func, *args, **kwargs):
    return None
