def find_call_targets(module: torch.fx.GraphModule):
    result = set()
    for n in module.graph.nodes:
        n: torch.fx.Node
        if n.op in {"call_module", "call_function", "call_method"}:
            result.add(n.target)
    return result
