@register_annotator("adaptive_avg_pool2d")
def _annotate_adaptive_avg_pool2d(
    gm: torch.fx.GraphModule,
    quantization_config: Optional[QuantizationConfig],
    filter_fn: Optional[Callable[[Node], bool]] = None,
) -> Optional[list[list[Node]]]:
    """Always annotate adaptive_avg_pool2d op"""
    module_partitions = get_source_partitions(
        gm.graph, [torch.nn.AdaptiveAvgPool2d, F.adaptive_avg_pool2d], filter_fn
    )
    partitions = list(itertools.chain.from_iterable(module_partitions.values()))
    annotated_partitions = []
    for partition in partitions:
        pool_node = partition.output_nodes[0]
        if (
            pool_node.op != "call_function"
            or pool_node.target != torch.ops.aten.adaptive_avg_pool2d.default
        ):
            raise ValueError(f"{pool_node} is not an aten adaptive_avg_pool2d operator")

        if _is_annotated([pool_node]):
            continue

        annotated_partitions.append(partition.nodes)
        input_act = pool_node.args[0]
        assert isinstance(input_act, Node)

        # only annotate input output sharing operator
        # when the output of the input node is annotated
        if (
            "quantization_annotation" not in input_act.meta
            or not input_act.meta["quantization_annotation"]._annotated
            or input_act.meta["quantization_annotation"].output_qspec is None
        ):
            input_act_qspec = get_input_act_qspec(quantization_config)
        else:
            input_act_qspec = SharedQuantizationSpec(input_act)

        # output sharing with input
        output_act_qspec = SharedQuantizationSpec((input_act, pool_node))
        pool_node.meta["quantization_annotation"] = QuantizationAnnotation(
            input_qspec_map={
                input_act: input_act_qspec,
            },
            output_qspec=output_act_qspec,
            _annotated=True,
        )
    return annotated_partitions
