def _detect_input_mutation(gm: torch.fx.GraphModule) -> bool:
    example_inputs = [
        ph.meta.get("val", None) for ph in gm.graph.find_nodes(op="placeholder")
    ]
    inp_mutation, _, _, _ = check_input_alias_and_mutation(gm, example_inputs)
    if len(inp_mutation) > 0:
        return True

    for _, module in gm.named_children():
        if isinstance(module, torch.fx.GraphModule):
            if _detect_input_mutation(module):
                return True

    return False
