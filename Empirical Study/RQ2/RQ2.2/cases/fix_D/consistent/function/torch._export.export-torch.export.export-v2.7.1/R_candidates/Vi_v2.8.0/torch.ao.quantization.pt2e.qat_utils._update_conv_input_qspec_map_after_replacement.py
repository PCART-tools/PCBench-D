def _update_conv_input_qspec_map_after_replacement(
    original_node: Node, replacement_node: Node
):
    """
    Update the `input_qspec_map` in the annotation after subgraph rewriting.

    The original annotation referred to the nodes in the original graph,
    so the keys in the `input_qspec_map` will need to be updated to reflect
    the corresponding nodes in the replacement graph.
    """
    assert _is_conv_or_conv_transpose_node(original_node)
    assert _is_conv_or_conv_transpose_node(replacement_node)
    if "quantization_annotation" not in original_node.meta:
        return
    original_input_qspec_map = original_node.meta[
        "quantization_annotation"
    ].input_qspec_map
    input_qspec_map = {}
    # get the list of configs, it should be ordered as input, weight, bias
    # note: this is really hacky, we need a better solution, hopefully
    # in subgraph_rewriter, issue tracking the problem: https://github.com/pytorch/pytorch/issues/101820
    all_configs = list(original_input_qspec_map.items())
    # input activation
    input_qspec_map[replacement_node.args[0]] = all_configs[0][1]
    # weight
    input_qspec_map[replacement_node.args[1]] = all_configs[1][1]
    # bias
    if len(replacement_node.args) > 2 and len(all_configs) > 2:
        input_qspec_map[replacement_node.args[2]] = all_configs[2][1]
    replacement_node.meta["quantization_annotation"].input_qspec_map = input_qspec_map
