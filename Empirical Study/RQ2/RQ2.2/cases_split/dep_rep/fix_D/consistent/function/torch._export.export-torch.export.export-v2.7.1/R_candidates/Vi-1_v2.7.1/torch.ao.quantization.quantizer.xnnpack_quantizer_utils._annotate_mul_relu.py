@register_annotator("mul_relu")
def _annotate_mul_relu(
    gm: torch.fx.GraphModule,
    quantization_config: Optional[QuantizationConfig],
    filter_fn: Optional[Callable[[Node], bool]] = None,
) -> Optional[list[list[Node]]]:
    annotated_partitions = []
    for node in gm.graph.nodes:
        if node.op != "call_function" or node.target not in [
            torch.ops.aten.relu.default,
            torch.ops.aten.relu_.default,
        ]:
            continue
        relu_node = node
        maybe_mul = node.args[0]
        if (
            not isinstance(maybe_mul, Node)
            or maybe_mul.op != "call_function"
            or maybe_mul.target
            not in [
                torch.ops.aten.mul.Tensor,
                torch.ops.aten.mul_.Tensor,
            ]
        ):
            continue

        mul_node = maybe_mul
        if len(mul_node.users) > 1:
            # mul can't be fused with ReLU if the result of mul is being used
            # else where in the graph
            continue

        partition = [relu_node, mul_node]

        if _is_annotated(partition):
            continue

        if filter_fn and any(not filter_fn(n) for n in partition):
            continue

        input_act_qspec = get_input_act_qspec(quantization_config)
        output_act_qspec = get_output_act_qspec(quantization_config)

        input_qspec_map = {}
        input_act0 = mul_node.args[0]
        if isinstance(input_act0, Node):
            if _is_input_large_scalar(input_act0, gm):
                continue
            if _is_input_non_float_tensor(input_act0):
                continue
            partition.append(input_act0)
            input_qspec_map[input_act0] = input_act_qspec

        input_act1 = mul_node.args[1]
        if isinstance(input_act1, Node):
            if _is_input_large_scalar(input_act1, gm):
                continue
            if _is_input_non_float_tensor(input_act1):
                continue
            partition.append(input_act1)
            input_qspec_map[input_act1] = input_act_qspec

        mul_node.meta["quantization_annotation"] = QuantizationAnnotation(
            input_qspec_map=input_qspec_map,
            _annotated=True,
        )
        relu_node.meta["quantization_annotation"] = QuantizationAnnotation(
            output_qspec=output_act_qspec,
            _annotated=True,
        )
        annotated_partitions.append(partition)
    return annotated_partitions
