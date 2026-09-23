def _detect_input_alias(gm: torch.fx.GraphModule) -> bool:
    example_inputs = [
        ph.meta.get("val", None) for ph in gm.graph.find_nodes(op="placeholder")
    ]
    _, inp_inp_alias_map, inp_out_alias_map, _ = check_input_alias_and_mutation(
        gm, example_inputs
    )
    if len(inp_out_alias_map) > 0 or len(inp_inp_alias_map) > 0:
        return True
    return False
