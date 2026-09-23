@register_decomposition([aten.detach, aten.lift, aten.lift_fresh])
@out_wrapper()
def nop_decomposition(x):
    return aten.alias(x)
