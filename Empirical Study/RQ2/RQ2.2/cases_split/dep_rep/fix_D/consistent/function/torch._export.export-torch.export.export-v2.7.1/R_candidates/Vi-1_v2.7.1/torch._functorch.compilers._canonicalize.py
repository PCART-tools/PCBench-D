def _canonicalize(fx_g):
    for node in fx_g.graph.find_nodes(
        op="call_function", target=torch.ops.aten._to_copy
    ):
        node.target = torch.ops.aten.to
    fx_g.recompile()
    return fx_g
