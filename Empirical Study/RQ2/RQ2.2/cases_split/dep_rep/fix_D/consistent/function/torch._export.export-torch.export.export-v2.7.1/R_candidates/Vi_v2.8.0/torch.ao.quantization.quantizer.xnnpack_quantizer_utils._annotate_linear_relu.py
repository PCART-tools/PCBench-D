@register_annotator("linear_relu")
def _annotate_linear_relu(
    gm: torch.fx.GraphModule,
    quantization_config: Optional[QuantizationConfig],
    filter_fn: Optional[Callable[[Node], bool]] = None,
) -> Optional[list[list[Node]]]:
    annotated_partitions = []
    input_act_qspec = get_input_act_qspec(quantization_config)
    output_act_qspec = get_output_act_qspec(quantization_config)
    weight_qspec = get_weight_qspec(quantization_config)
    bias_qspec = get_bias_qspec(quantization_config)
    for node in gm.graph.nodes:
        if node.op != "call_function" or node.target not in [
            torch.ops.aten.relu.default,
            torch.ops.aten.relu_.default,
        ]:
            continue
        relu_node = node
        maybe_linear_node = node.args[0]
        if (
            not isinstance(maybe_linear_node, Node)
            or maybe_linear_node.op != "call_function"
            or maybe_linear_node.target != torch.ops.aten.linear.default
        ):
            continue

        linear_node = maybe_linear_node
        if len(linear_node.users) > 1:
            # if linear node has multiple users, then it can't be fused with relu
            continue

        input_qspec_map = {}
        input_act = linear_node.args[0]
        assert isinstance(input_act, Node)
        input_qspec_map[input_act] = input_act_qspec

        weight = linear_node.args[1]
        assert isinstance(weight, Node)
        input_qspec_map[weight] = weight_qspec

        # adding weight node to the partition as well
        partition = [relu_node, linear_node, weight]
        bias = linear_node.args[2] if len(linear_node.args) > 2 else None
        if isinstance(bias, Node):
            input_qspec_map[bias] = bias_qspec
            partition.append(bias)

        if _is_annotated(partition):
            continue

        if filter_fn and any(not filter_fn(n) for n in partition):
            continue

        linear_node.meta["quantization_annotation"] = QuantizationAnnotation(
            input_qspec_map=input_qspec_map,
            _annotated=True,
        )
        relu_node.meta["quantization_annotation"] = QuantizationAnnotation(
            output_qspec=output_act_qspec,
            _annotated=True,
        )
        _mark_nodes_as_annotated(partition)
        annotated_partitions.append(partition)
    return annotated_partitions
