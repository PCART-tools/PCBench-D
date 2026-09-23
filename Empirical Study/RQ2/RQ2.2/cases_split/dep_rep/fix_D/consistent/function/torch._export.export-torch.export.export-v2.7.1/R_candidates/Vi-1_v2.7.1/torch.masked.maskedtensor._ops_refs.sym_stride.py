@register_dispatch_func([torch.ops.aten.sym_stride])
def sym_stride(func, *args, **kwargs):
    return None
