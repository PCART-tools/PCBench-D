def get_ep_stats(ep: ExportedProgram) -> dict[str, Any]:
    op_count = 0
    op_set = set()
    for m in ep.graph_module.modules():
        if not isinstance(m, torch.fx.GraphModule):
            continue
        for node in m.graph.nodes:
            if node.op != "call_function":
                continue
            op_count += 1
            assert hasattr(node.target, "__module__")
            assert hasattr(node.target, "__name__")
            op_set.add(f"{node.target.__module__}.{node.target.__name__}")
    return {"op_count": op_count, "op_set": op_set}
