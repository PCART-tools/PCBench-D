def _annotate_nodes_not_quantize(nodes: Union[Node, list[Node]]) -> None:
    """Annotate nodes to exclude them from quantization (their `quantization_config` is `None`)."""
    if not isinstance(nodes, list):
        nodes = [nodes]
    for node in nodes:
        node.meta[QUANT_ANNOTATION_KEY] = _X86InductorQuantizationAnnotation(
            _annotated=True
        )
