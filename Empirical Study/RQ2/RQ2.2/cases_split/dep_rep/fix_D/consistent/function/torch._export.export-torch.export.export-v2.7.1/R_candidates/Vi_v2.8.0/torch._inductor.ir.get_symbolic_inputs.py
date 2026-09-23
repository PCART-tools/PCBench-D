def get_symbolic_inputs(inputs: list[Buffer]) -> list[Expr]:
    sym_vars: OrderedSet[Expr] = OrderedSet()
    for inp in inputs:
        sym_vars |= get_free_symbols(inp.get_size(), unbacked_only=False)
        sym_vars |= get_free_symbols(inp.get_stride(), unbacked_only=False)

    return list(sym_vars)
