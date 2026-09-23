@register_lowering(aten.sym_stride.int)
def sym_stride(a, dim):
    val = V.graph.current_node.meta["val"]
    # See Note [Can val be an int?]
    assert isinstance(val, torch.SymInt)
    return val.node.expr
