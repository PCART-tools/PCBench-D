def find_symbol_binding_fx_nodes(
    graph: torch.fx.Graph,
) -> dict[sympy.Symbol, torch.fx.Node]:
    r = {}
    # NB: Prefer first occurrence of symbol
    for node in graph.nodes:
        if (s := is_symbol_binding_fx_node(node)) is not None and s not in r:
            r[s] = node
    return r
