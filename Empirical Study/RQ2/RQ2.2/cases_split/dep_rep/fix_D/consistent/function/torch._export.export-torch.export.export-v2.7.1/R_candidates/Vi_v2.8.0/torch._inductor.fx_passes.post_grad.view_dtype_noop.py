@register_noop_decomp(aten.view.dtype)
def view_dtype_noop(arg, dtype):
    return arg.dtype == dtype
