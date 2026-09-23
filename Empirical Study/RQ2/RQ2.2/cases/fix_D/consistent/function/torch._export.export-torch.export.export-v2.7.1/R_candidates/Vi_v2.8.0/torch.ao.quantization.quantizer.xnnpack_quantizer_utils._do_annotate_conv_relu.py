def _do_annotate_conv_relu(
    gm: torch.fx.GraphModule,
    quantization_config: Optional[QuantizationConfig],
    filter_fn: Optional[Callable[[Node], bool]] = None,
    is_conv_transpose: bool = False,
):
    annotated_partitions = []
    for n in gm.graph.nodes:
        if n.op != "call_function" or n.target not in [
            torch.ops.aten.relu.default,
            torch.ops.aten.relu_.default,
        ]:
            continue
        relu_node = n
        maybe_conv_node = n.args[0]

        is_conv_node = _is_conv_transpose_node if is_conv_transpose else _is_conv_node
        if not isinstance(maybe_conv_node, Node) or not is_conv_node(maybe_conv_node):
            continue
        conv_node = maybe_conv_node

        if len(conv_node.users) > 1:
            # relu shouldn't be fuseable to conv if there are other users
            # of convolution
            continue

        input_qspec_map = {}
        input_act = conv_node.args[0]
        assert isinstance(input_act, Node)
        input_qspec_map[input_act] = get_input_act_qspec(quantization_config)

        weight = conv_node.args[1]
        assert isinstance(weight, Node)
        input_qspec_map[weight] = get_weight_qspec(quantization_config)

        # adding weight node to the partition as well
        partition = [relu_node, conv_node, conv_node.args[1]]
        bias = conv_node.args[2] if len(conv_node.args) > 2 else None
        if isinstance(bias, Node):
            input_qspec_map[bias] = get_bias_qspec(quantization_config)
            partition.append(bias)

        if _is_annotated(partition):
            continue

        if filter_fn and any(not filter_fn(n) for n in partition):
            continue

        conv_node.meta["quantization_annotation"] = QuantizationAnnotation(
            input_qspec_map=input_qspec_map, _annotated=True
        )
        relu_node.meta["quantization_annotation"] = QuantizationAnnotation(
            output_qspec=get_output_act_qspec(quantization_config),  # type: ignore[arg-type]
            _annotated=True,
        )
        _mark_nodes_as_annotated(partition)
        annotated_partitions.append(partition)
    return annotated_partitions
