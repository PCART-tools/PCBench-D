@register_lowering(prims.copy_strided.default)
def copy_strided(x, stride):
    stride = [V.graph.sizevars.size_hint(s) for s in stride]
    stride_order = sorted(range(len(stride)), key=stride.__getitem__)
    return ir.ExternKernel.require_stride_order(x, stride_order)
