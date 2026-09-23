def _extract_fwd_bwd_outputs(
    joint_module: fx.GraphModule, *, num_fwd_outputs
) -> tuple[list[fx.Node], list[fx.Node]]:
    outputs = pytree.arg_tree_leaves(
        *(node.args for node in joint_module.graph.find_nodes(op="output"))
    )
    fwd_outputs = outputs[:num_fwd_outputs]
    bwd_outputs = outputs[num_fwd_outputs:]
    return fwd_outputs, bwd_outputs
