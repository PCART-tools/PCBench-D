def sym_sum(args):
    """
    N-ary add which is faster to compute for long lists than iterated binary
    addition.  Only does something special for integers.
    """
    if overrides.has_torch_function(args):
        return overrides.handle_torch_function(sym_sum, args, args)

    found = None
    for a in args:
        if not isinstance(a, (SymInt, builtins.int)):
            return builtins.sum(args)
        if isinstance(a, SymInt):
            found = a.node
    if found is None:
        return builtins.sum(args)

    from torch.fx.experimental.sym_node import to_node, wrap_node

    return wrap_node(found.sym_sum(tuple(to_node(found, a) for a in args)))
