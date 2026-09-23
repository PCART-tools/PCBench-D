@register_decomposition([aten._reshape_alias, aten._unsafe_view])
@out_wrapper()
def _reshape_alias(x, shape, *args):
    return aten.view(x, shape)
