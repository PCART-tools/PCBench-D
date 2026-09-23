@register_lowering(aten.sym_size.int)
def sym_size(a, dim):
    val = V.graph.current_node.meta["val"]
    # Note [Can val be an int?]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # In principle, someone could construct an FX graph where
    # a call to size/stride has a val that is a plain int (not
    # SymInt).  However, we will maintain the invariant that
    # this is not possible: if you are constructing an FX graph
    # where there is a call to size/stride that returns an
    # int, but you KNOW that int must always be a constant,
    # then you do not need trace that call at all (and just
    # constant propagate the integer as is.)
    assert isinstance(val, torch.SymInt)
    return val.node.expr
