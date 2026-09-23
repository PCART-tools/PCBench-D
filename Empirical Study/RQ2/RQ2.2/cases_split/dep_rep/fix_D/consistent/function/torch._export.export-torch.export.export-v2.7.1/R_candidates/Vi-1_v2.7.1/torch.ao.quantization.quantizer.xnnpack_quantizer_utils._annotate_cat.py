@register_annotator("cat")
def _annotate_cat(
    gm: torch.fx.GraphModule,
    quantization_config: Optional[QuantizationConfig],
    filter_fn: Optional[Callable[[Node], bool]] = None,
) -> Optional[list[list[Node]]]:
    cat_partitions = get_source_partitions(gm.graph, [torch.cat], filter_fn)
    cat_partitions = list(itertools.chain.from_iterable(cat_partitions.values()))
    annotated_partitions = []
    for cat_partition in cat_partitions:
        cat_node = cat_partition.output_nodes[0]
        if _is_annotated([cat_node]):
            continue

        if cat_node.target != torch.ops.aten.cat.default:
            # TODO: change this to AnnotationException
            raise Exception(  # noqa: TRY002
                f"Expected cat node: torch.ops.aten.cat.default, but found {cat_node.target}"
                " please check if you are calling the correct capture API"
            )

        annotated_partitions.append(cat_partition.nodes)

        input_act_qspec = get_input_act_qspec(quantization_config)
        inputs = cat_node.args[0]

        input_qspec_map = {}
        input_act0 = inputs[0]  # type: ignore[index]
        if isinstance(input_act0, Node):
            input_qspec_map[input_act0] = input_act_qspec

        shared_with_input0_qspec = SharedQuantizationSpec((input_act0, cat_node))  # type: ignore[arg-type]
        for input_act in inputs[1:]:  # type: ignore[index, union-attr]
            if input_act not in input_qspec_map:
                input_qspec_map[input_act] = shared_with_input0_qspec  # type: ignore[index]

        output_act_qspec = shared_with_input0_qspec

        cat_node.meta["quantization_annotation"] = QuantizationAnnotation(
            input_qspec_map=input_qspec_map,
            output_qspec=output_act_qspec,
            _annotated=True,
        )
    return annotated_partitions
