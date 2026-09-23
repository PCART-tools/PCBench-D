@register_jagged_func(torch.ops.aten._nested_get_jagged_dummy.default, "self: any")
def _nested_get_jagged_dummy(func, *args, **kwargs):
    from torch.nested._internal.nested_tensor import _nt_view_dummy

    return _nt_view_dummy()
