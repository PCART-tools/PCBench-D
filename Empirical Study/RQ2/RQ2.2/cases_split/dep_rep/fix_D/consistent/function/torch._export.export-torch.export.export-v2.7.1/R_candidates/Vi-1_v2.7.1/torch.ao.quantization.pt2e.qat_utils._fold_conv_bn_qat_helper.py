def _fold_conv_bn_qat_helper(
    m: GraphModule,
    conv_fn: Callable,
    example_inputs: tuple[Any, ...],
    is_cuda: bool,
) -> GraphModule:
    """
    Replace the quantized (conv + bn) pattern with conv with bn weights folded into the weights of conv.
    """

    m.graph.eliminate_dead_code()
    m.recompile()
    _duplicate_dequantize_node(m)

    # Step (1): Replace QAT pattern with simple [conv - bn] pattern
    replacements = []
    replacement_options = itertools.product(
        [True, False],  # is_per_channel
        [True, False],  # has_bias
        [True, False],  # bias_is_quantized
        [True, False],  # bn_is_training
    )
    for (
        is_per_channel,
        has_bias,
        bias_is_quantized,
        bn_is_training,
    ) in replacement_options:
        # For the cases without bias, `bias_is_quantized` is irrelevant, so here we arbitrarily
        # filter out one of the values for this flag to avoid having duplicate patterns
        if not has_bias and bias_is_quantized:
            continue
        kwargs = _get_quantized_conv_bn_example_inputs_kwargs(
            is_per_channel, has_bias, bias_is_quantized, is_cuda
        )
        match_pattern = _get_quantized_qat_conv_bn_pattern(
            is_per_channel, has_bias, bias_is_quantized, conv_fn, bn_is_training
        )
        match_pattern = _get_aten_graph_module_for_pattern(
            match_pattern,
            example_inputs,
            is_cuda,
            **kwargs,
        )
        replacement_pattern = _get_folded_quantized_qat_conv_bn_pattern(
            is_per_channel, has_bias, bias_is_quantized, conv_fn, bn_is_training
        )
        replacement_pattern = _get_aten_graph_module_for_pattern(
            replacement_pattern,
            example_inputs,
            is_cuda,
            **kwargs,
        )
        replacements.extend(
            replace_pattern_with_filters(
                m,
                match_pattern,
                replacement_pattern,
                ignore_literals=True,
            )
        )
    m.recompile()
    _remove_extra_dequantize(m)

    for r in replacements:
        node_map = _get_conv_bn_pattern_nodes(r)

        # Step (2): Copy over metadata from original subgraph
        for original_node, replacement_node in node_map.values():
            replacement_node.meta = original_node.meta

        # Step (3): Copy over args for weight (and optionally bias) q - dq nodes
        _copy_over_q_dq_args(*node_map["conv_weight_q"])
        _copy_over_q_dq_args(*node_map["conv_weight_dq"])
        if "conv_bias_q" in node_map:
            assert "conv_bias_dq" in node_map
            _copy_over_q_dq_args(*node_map["conv_bias_q"])
            _copy_over_q_dq_args(*node_map["conv_bias_dq"])

        # Step (4): Fold BN weights into conv
        conv_bias = None
        (_, conv_node) = node_map["conv"]
        (_, bn_node) = node_map["bn"]
        (_, conv_weight) = node_map["conv_weight"]
        if "conv_bias" in node_map:
            (_, conv_bias) = node_map["conv_bias"]
        fold_bn_weights_into_conv_node(conv_node, conv_weight, conv_bias, bn_node, m)

        # Copy over literal args for conv
        for original_node in _filter_nodes_map(r.nodes_map).values():
            if _is_conv_or_conv_transpose_node(original_node):
                _copy_over_literal_conv_args(original_node, conv_node)

    m.graph.eliminate_dead_code()
    m.recompile()
    return m
