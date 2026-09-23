@register_noop_decomp(aten.view)
def view_noop(arg, size):
    return arg.shape == size
