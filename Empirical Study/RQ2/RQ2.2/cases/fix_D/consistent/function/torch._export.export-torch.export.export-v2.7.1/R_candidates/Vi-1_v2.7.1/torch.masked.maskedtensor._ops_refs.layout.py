@register_dispatch_func([torch.ops.prim.layout])
def layout(func, *args, **kwargs):
    return _get_data(args[0]).layout
