def _fuse_conv_bn_qat_helper(
    m: GraphModule,
    conv_fn: Callable,
    example_inputs: tuple[Any, ...],
    is_cuda: bool,
) -> GraphModule:
    """
    Given a graph of decomposed aten ops, replace the (conv + bn) pattern with
    the fused QAT subgraph equivalent. The input graph should already be annotated.
    The annotations in the original nodes will be preserved in the corresponding
    nodes in the new subgraph.

    Note: This also handles the (conv + bn + relu) pattern.
    """
    m.graph.eliminate_dead_code()
    m.recompile()

    conv_bn_pattern = _get_conv_bn_pattern(conv_fn)
    match_pattern = _get_aten_graph_module_for_pattern(
        conv_bn_pattern,
        example_inputs,
        is_cuda,
    )

    # Step (1): Replace patterns with conv bias
    #
    # Here we do replacement separately for cases with and without conv bias, since
    # the replacement patterns for these two cases are substantially different.
    # TODO: use the public replace_pattern API once it also returns replacement nodes

    qat_conv_bn_pattern = _get_qat_conv_bn_pattern(conv_fn)
    replacement_pattern_with_conv_bias = _get_aten_graph_module_for_pattern(
        qat_conv_bn_pattern,
        example_inputs,
        is_cuda,
    )
    replacements_with_conv_bias = replace_pattern_with_filters(
        m,
        match_pattern,
        replacement_pattern_with_conv_bias,
        match_filters=[_has_conv_bias_filter],
        ignore_literals=True,
    )
    m.recompile()

    # Step (2): Replace patterns without conv bias

    qat_conv_bn_pattern_no_conv_bias = _get_qat_conv_bn_pattern_no_conv_bias(conv_fn)
    replacement_pattern_no_conv_bias = _get_aten_graph_module_for_pattern(
        qat_conv_bn_pattern_no_conv_bias,
        example_inputs,
        is_cuda,
    )
    replacements_no_conv_bias = replace_pattern_with_filters(
        m,
        match_pattern,
        replacement_pattern_no_conv_bias,
        match_filters=[_no_conv_bias_filter],
        ignore_literals=True,
    )
    m.recompile()

    # Step (3): Post processing
    #
    # Due to limited functionality in the subgraph rewriter, here we manually
    # update the replacement graph as follows:
    #
    #   (a) Copy over metadata from original subgraph. This ensures the stack traces
    #       and annotations are preserved in the new subgraph
    #
    #   (b) Copy over literal args for conv from the original subgraph
    #       TODO: do this for literal args for batchnorm as well
    #
    #   (c) Update all references of the old nodes in the original subgraph to refer
    #       to the corresponding nodes in the new subgraph in the annotations
    #
    # In the future, we should try to push as much of this functionality into the
    # subgraph rewriter as possible, so we don't have to manually copy anything over.
    # For more detail, see https://github.com/pytorch/pytorch/issues/100419.

    all_original_to_replacement_nodes = {}
    for r in replacements_with_conv_bias + replacements_no_conv_bias:
        replacement_dict = _get_conv_bn_pattern_nodes(r)
        # The original conv node's "nn_module_stack"
        conv_nn_module = replacement_dict["conv"][0].meta.get("nn_module_stack", None)
        for k, node_tuple in replacement_dict.items():
            original_node, replacement_node = node_tuple
            # Step (3a): Copy over metadata for all nodes in [conv - bn - getitem]
            replacement_node.meta = original_node.meta
            # If original_node is a get_attr node, it doesn't have nn_module_stack.
            # In this case, we copy nn_module_stack from the original conv node.
            if (
                k in ["conv_input", "conv_weight"]
                and conv_nn_module
                and "nn_module_stack" not in replacement_node.meta
            ):
                replacement_node.meta["nn_module_stack"] = copy.deepcopy(conv_nn_module)
            if _is_conv_or_conv_transpose_node(original_node):
                # Step (3b): Copy over conv literal args
                _copy_over_literal_conv_args(original_node, replacement_node)
                # Step (3c): Update old references in the conv node's input_qspec_map
                _update_conv_input_qspec_map_after_replacement(
                    original_node, replacement_node
                )
            all_original_to_replacement_nodes[original_node] = replacement_node

    # Step (3c): Update old references in the special qspecs for all nodes in the graph
    for n in m.graph.nodes:
        _update_special_qspecs_after_replacement(n, all_original_to_replacement_nodes)

    return m
